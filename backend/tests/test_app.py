from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from backend.app import app, load_model_bundle


@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def build_sample_payload() -> dict:
    dataset_path = Path(__file__).resolve().parents[2] / "creditcard.csv"
    df = pd.read_csv(dataset_path)
    sample = df.drop(columns=["Class"]).iloc[0].to_dict()
    return {key: float(value) for key, value in sample.items()}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_predict_success(client):
    payload = build_sample_payload()
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.get_json()
    assert "prediction" in body
    assert body["label"] in {"fraud", "non_fraud"}


def test_invalid_json(client):
    response = client.post("/predict", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert "JSON object" in response.get_json()["error"]


def test_missing_feature(client):
    payload = build_sample_payload()
    payload.pop("Amount")
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert "Missing required feature" in response.get_json()["error"]


def test_model_loading_failure():
    with pytest.raises(FileNotFoundError):
        load_model_bundle(Path("path-does-not-exist.joblib"))
