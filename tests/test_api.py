import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from src.api import (
    ClauseSearchRequest,
    ContractIndexRequest,
    health_check,
    index_contract,
    search_contract_clauses,
)


class ApiTests(unittest.TestCase):
    def test_health_endpoint(self):
        self.assertEqual(health_check(), {"status": "ok"})

    @patch("src.api.add_text_chunks")
    @patch("src.api.get_collection")
    def test_index_contract_stores_heading_metadata(
        self,
        get_collection,
        add_text_chunks,
    ):
        collection = Mock()
        collection.count.return_value = 0
        get_collection.return_value = collection

        response = index_contract(
            ContractIndexRequest(
                source="contract.txt",
                text="DUTIES: Provider performs services.\n"
                "LIABILITY: Liability is capped.",
            )
        )

        self.assertTrue(response.contract_id.startswith("contract_"))
        self.assertEqual(response.indexed_sections, 2)
        add_text_chunks.assert_called_once()
        self.assertEqual(
            add_text_chunks.call_args.args[1],
            ["DUTIES", "LIABILITY"],
        )

    @patch("src.api.search_similar_clauses")
    @patch("src.api.get_collection")
    def test_search_endpoint_returns_retrieved_clauses(
        self,
        get_collection,
        search_similar_clauses,
    ):
        collection = Mock()
        collection.count.return_value = 1
        get_collection.return_value = collection
        search_similar_clauses.return_value = [{"heading": "TERMINATION"}]

        response = search_contract_clauses(
            ClauseSearchRequest(
                contract_id="contract_" + ("a" * 32),
                question="What are the termination rights?",
            )
        )

        self.assertEqual(response, {"results": [{"heading": "TERMINATION"}]})
        search_similar_clauses.assert_called_once_with(
            "What are the termination rights?",
            collection=collection,
            top_k=3,
        )

    @patch("src.api.get_collection")
    def test_search_returns_not_found_for_unindexed_contract(self, get_collection):
        collection = Mock()
        collection.count.return_value = 0
        get_collection.return_value = collection

        with self.assertRaises(HTTPException) as error:
            search_contract_clauses(
                ClauseSearchRequest(
                    contract_id="contract_" + ("b" * 32),
                    question="What does the term section say?",
                )
            )

        self.assertEqual(error.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
