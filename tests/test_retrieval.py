import unittest
from unittest.mock import patch

from src.utils.document_processor import DocumentProcessor
from src.utils.vector_store import search_similar_clauses


class _Embedding:
    def tolist(self):
        return [0.1, 0.2]


class _EmbeddingModel:
    def encode(self, _text, convert_to_numpy):
        return _Embedding()


class _Collection:
    def __init__(self):
        self.query_count = None

    def count(self):
        return 4

    def query(self, query_embeddings, n_results, include):
        self.query_count = n_results
        return {
            "ids": [["general-1", "liability", "general-2", "termination"]],
            "documents": [[
                "General one",
                "Liability clause",
                "General two",
                "Termination clause",
            ]],
            "metadatas": [
                [
                    {"heading": "General contract text", "source": "contract"},
                    {"heading": "LIMITATION OF LIABILITY", "source": "contract"},
                    {"heading": "General contract text", "source": "contract"},
                    {"heading": "TERMINATION", "source": "contract"},
                ]
            ],
            "distances": [[0.05, 0.7, 0.2, 0.5]],
        }


class _HeadingCollection:
    def __init__(self, heading):
        self.heading = heading

    def count(self):
        return 2

    def query(self, query_embeddings, n_results, include):
        return {
            "ids": [["general", "specific"]],
            "documents": [["General text", "Specific clause"]],
            "metadatas": [[
                {"heading": "General contract text", "source": "contract"},
                {"heading": self.heading, "source": "contract"},
            ]],
            "distances": [[0.05, 0.8]],
        }


class DocumentChunkingTests(unittest.TestCase):
    def test_chunks_at_requested_legal_headings(self):
        text = "\n".join(
            [
                "Opening language.",
                "DUTIES: Provider will perform services.",
                "COMPENSATION: Client will pay the fee.",
                "TERM: This agreement lasts one year.",
                "TERMINATION: Either party may terminate.",
                "LIABILITY: Liability is capped.",
                "SAFETY: Provider follows safety rules.",
                "INDEMNIFICATION: Provider will indemnify Client.",
            ]
        )

        chunks = DocumentProcessor.chunk_text(text)

        self.assertEqual(len(chunks), 8)
        self.assertEqual(
            [DocumentProcessor.get_chunk_heading(chunk) for chunk in chunks[1:]],
            [
                "DUTIES",
                "COMPENSATION",
                "TERM",
                "TERMINATION",
                "LIABILITY",
                "SAFETY",
                "INDEMNIFICATION",
            ],
        )

    def test_matching_heading_outranks_closer_general_semantic_result(self):
        collection = _Collection()

        with patch(
            "src.utils.vector_store._get_embedding_model",
            return_value=_EmbeddingModel(),
        ):
            results = search_similar_clauses(
                "What is the liability cap?",
                collection=collection,
                top_k=2,
            )

        self.assertEqual(collection.query_count, 4)
        self.assertEqual(results[0]["id"], "liability")
        self.assertEqual(results[1]["id"], "general-1")

    def test_metadata_reranking_covers_all_requested_heading_types(self):
        cases = [
            ("What are the provider's duties?", "DUTIES"),
            ("What is the compensation?", "COMPENSATION"),
            ("What is the contract term?", "TERM"),
            ("What are the termination rights?", "TERMINATION"),
            ("What is the liability cap?", "LIABILITY"),
            ("What are the safety rules?", "SAFETY"),
            ("What is the indemnification obligation?", "INDEMNIFICATION"),
        ]

        for query, heading in cases:
            with self.subTest(heading=heading), patch(
                "src.utils.vector_store._get_embedding_model",
                return_value=_EmbeddingModel(),
            ):
                results = search_similar_clauses(
                    query,
                    collection=_HeadingCollection(heading),
                    top_k=1,
                )

            self.assertEqual(results[0]["id"], "specific")


if __name__ == "__main__":
    unittest.main()
