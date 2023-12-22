import pytest
from fastapi.testclient import TestClient
import time


from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_invalid_questions_file():
    response = client.post(
        "/answer",
        files=[
            ("source_file", open("samples/e1source.json", "rb")),
            ("question_file", open("samples/invalid-questions.json", "rb")),
        ],
    )
    assert response.status_code == 400


def test_invalid_source_file():
    response = client.post(
        "/answer",
        files=[
            ("source_file", open("samples/sample.txt", "rb")),
            ("question_file", open("samples/e1questions.json", "rb")),
        ],
    )
    assert response.status_code == 400


@pytest.mark.skip(reason="Integration test requires higher OpenAI rate limit")
def test_answer_with_source_json():
    time.sleep(30)  # wait to avoid openai rate limit
    response = client.post(
        "/answer",
        files=[
            ("source_file", open("samples/e1source.json", "rb")),
            ("question_file", open("samples/e1questions.json", "rb")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "When do employees get time off?": "Employees get time off to vote.",
        "How many times do we conduct Incident Response Program?": "The Incident Response Program is conducted at least once a year.",
    }


@pytest.mark.skip(reason="Integration test requires higher OpenAI rate limit")
def test_answer_with_source_pdf():
    time.sleep(30)  # wait to avoid openai rate limit
    response = client.post(
        "/answer",
        files=[
            ("source_file", open("samples/e2source.pdf", "rb")),
            ("question_file", open("samples/e2questions.json", "rb")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "What is the page count?": "The page count is not specified in the given context.",
        "What is this text about?": "The text is about a simple PDF file that is being used for demonstration purposes in Virtual Mechanics tutorials.",
    }
