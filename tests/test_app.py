# test_app.py
import pytest
import pandas as pd
from app.main import get_ai_response
from evaluation.evaluator import evaluate_response



# Load test data
test_data = pd.read_csv("data/test_cases.csv")

@pytest.mark.parametrize("query", test_data[["query"]].values)
def test_ai_responses_quality(query):
    response = get_ai_response(query)
    evaluation = evaluate_response(query, response)
    print("\nEvaluation:\n", evaluation)

    # Extract score (simple parsing)
    score_line = evaluation.split("\n")[0]
    score = int(score_line.split(":")[1].strip())

    assert score >= 3, f"Score {score} is below minimum required (3)"


# @pytest.mark.parametrize("query,expected_keyword", test_data[["query", "expected_keyword"]].values)
# def test_ai_responses(query, expected_keyword):
#     response = get_ai_response(query)
    
#     assert expected_keyword.lower() in response.lower()

# def test_refund_policy_exists():
#     query = "What is the refund policy?"
#     response = get_ai_response(query)
#     assert response is not None

# def test_refund_policy_contains_keywords():
#     query = "What is the refund policy?"
#     response = get_ai_response(query)
#     assert "refund" in response.lower()

# def test_ambiguous_query():
#     query = "can I return it?"
#     response = get_ai_response(query)
#     assert response is not None


# def test_invalid_refund():
#     query = "Can I get a refund without buying anything?"
#     response = get_ai_response(query)
    
#     assert response is not None
    
# touch app/__init__.py
# From repo root (venv has pytest): ./venv/bin/python -m pytest
