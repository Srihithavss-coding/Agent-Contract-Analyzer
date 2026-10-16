"""FastAPI endpoints for indexing and retrieving contract clauses."""

import hashlib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.utils.document_processor import DocumentProcessor
from src.utils.vector_store import (
    add_text_chunks,
    get_collection,
    search_similar_clauses,
)


app = FastAPI(
    title="Contract Analyzer API",
    description="Index contracts and retrieve clauses with semantic and heading-aware search.",
    version="1.0.0",
)


class ContractIndexRequest(BaseModel):
    source: str = Field(min_length=1, max_length=255)
    text: str = Field(min_length=1, max_length=1_000_000)


class ContractIndexResponse(BaseModel):
    contract_id: str
    indexed_sections: int


class ClauseSearchRequest(BaseModel):
    contract_id: str = Field(pattern=r"^contract_[a-f0-9]{32}$")
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=20)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/contracts/index", response_model=ContractIndexResponse)
def index_contract(request: ContractIndexRequest) -> ContractIndexResponse:
    if not request.source.strip():
        raise HTTPException(status_code=422, detail="source must not be blank.")

    chunks = DocumentProcessor.chunk_text(request.text)
    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No searchable contract text was found.",
        )

    digest = hashlib.sha256(
        request.source.encode("utf-8") + b"\0" + request.text.encode("utf-8")
    ).hexdigest()[:32]
    contract_id = f"contract_{digest}"
    headings = [DocumentProcessor.get_chunk_heading(chunk) for chunk in chunks]

    try:
        collection = get_collection(contract_id)
        if collection.count() == 0:
            add_text_chunks(chunks, headings, request.source, collection)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not index contract: {exc}",
        ) from exc

    return ContractIndexResponse(contract_id=contract_id, indexed_sections=len(chunks))


@app.post("/clauses/search")
def search_contract_clauses(request: ClauseSearchRequest) -> dict[str, object]:
    try:
        collection = get_collection(request.contract_id)
        if collection.count() == 0:
            raise HTTPException(status_code=404, detail="Indexed contract was not found.")
        results = search_similar_clauses(
            request.question,
            collection=collection,
            top_k=request.top_k,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not search clauses: {exc}",
        ) from exc

    return {"results": results}
