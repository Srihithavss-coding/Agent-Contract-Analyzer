"""Semantic storage and retrieval for contract clauses."""

from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence
from uuid import uuid4

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer


DEFAULT_COLLECTION_NAME = "contract_clauses"
DEFAULT_PERSIST_DIRECTORY = Path("./chroma_db")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_RESULT_COUNT = 3


@lru_cache(maxsize=1)
def _get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once, on first use."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_directory: str | Path = DEFAULT_PERSIST_DIRECTORY,
) -> Collection:
    """Open or create a persistent ChromaDB collection for contract clauses."""
    if not collection_name.strip():
        raise ValueError("collection_name must not be empty")

    try:
        # Chroma creates the persistence directory if it does not already exist.
        client = chromadb.PersistentClient(path=str(persist_directory))
        return client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
    except Exception as exc:
        raise RuntimeError(
            f"Could not initialize ChromaDB collection '{collection_name}': {exc}"
        ) from exc


def add_text_chunks(
    chunks: Sequence[str],
    headings: Sequence[str],
    source: str,
    collection: Collection | None = None,
) -> list[str]:
    """Embed and store clause chunks with their legal headings and source."""
    if len(chunks) != len(headings):
        raise ValueError("chunks and headings must contain the same number of items")
    if not source.strip():
        raise ValueError("source must not be empty")
    if not chunks:
        return []
    if any(not chunk.strip() for chunk in chunks):
        raise ValueError("chunks must not contain empty text")
    if any(not heading.strip() for heading in headings):
        raise ValueError("headings must not contain empty text")

    target_collection = collection if collection is not None else get_collection()
    ids = [str(uuid4()) for _ in chunks]
    documents = [chunk.strip() for chunk in chunks]
    metadatas = [
        {"heading": heading.strip(), "source": source.strip()}
        for heading in headings
    ]

    try:
        # Compute vectors with the same model used to embed search queries.
        embeddings = _get_embedding_model().encode(
            documents,
            convert_to_numpy=True,
        ).tolist()
        target_collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        return ids
    except Exception as exc:
        raise RuntimeError(f"Could not add contract chunks to ChromaDB: {exc}") from exc


def search_similar_clauses(
    query: str,
    collection: Collection | None = None,
    top_k: int = DEFAULT_RESULT_COUNT,
) -> list[dict[str, Any]]:
    """Return the most semantically similar clauses, including their metadata."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    target_collection = collection if collection is not None else get_collection()
    try:
        # Encode the question into the same vector space as the stored clauses.
        query_embedding = _get_embedding_model().encode(
            query.strip(),
            convert_to_numpy=True,
        ).tolist()
        results = target_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        # Chroma returns one result list per query; this function submits one query.
        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []
        ids = results["ids"][0] if results["ids"] else []
        return [
            {
                "id": ids[index],
                "heading": (metadatas[index] or {}).get("heading"),
                "text": document,
                "source": (metadatas[index] or {}).get("source"),
                "distance": distances[index],
            }
            for index, document in enumerate(documents)
        ]
    except Exception as exc:
        raise RuntimeError(f"Could not search contract clauses: {exc}") from exc