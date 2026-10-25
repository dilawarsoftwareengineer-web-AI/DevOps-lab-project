from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "model_bundle.joblib"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def load_model_bundle(model_path: Path | str = MODEL_PATH) -> dict[str, Any]:
    bundle_path = Path(model_path)
    if not bundle_path.exists():
        raise FileNotFoundError(f"Model bundle not found at {bundle_path}")
    bundle = joblib.load(bundle_path)
    if not isinstance(bundle, dict):
        raise TypeError("Model bundle must be a dictionary containing a trained pipeline.")
    pipeline = bundle.get("pipeline")
    if pipeline is None:
        raise ValueError("Model bundle does not contain a trained pipeline under the 'pipeline' key.")
    return bundle


MODEL_BUNDLE = None
try:
    MODEL_BUNDLE = load_model_bundle()
except FileNotFoundError as exc:
    logger.warning("Model bundle could not be loaded at startup: %s", exc)
except Exception as exc:  # pragma: no cover - startup safety
    logger.warning("Unexpected model-load failure at startup: %s", exc)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    def model_metadata() -> dict[str, Any]:
        bundle = MODEL_BUNDLE
        if bundle is None:
            raise RuntimeError("Model bundle is not available.")
        return {
            "task": bundle.get("task", "binary_classification"),
            "target": bundle.get("target", "Class"),
            "model_name": bundle.get("model_name", "unknown"),
            "model_version": bundle.get("model_version", "unknown"),
            "feature_names": list(bundle.get("feature_names", [])),
            "package_versions": bundle.get("package_versions", {}),
            "metrics": bundle.get("metrics", {}),
        }

    @app.route("/health", methods=["GET"])
    def health() -> tuple[Any, int]:
        try:
            metadata = model_metadata()
            return (
                jsonify(
                    {
                        "status": "ok",
                        "message": "Fraud detection model API is running.",
                        "model_loaded": True,
                        **metadata,
                    }
                ),
                200,
            )
        except RuntimeError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Model bundle is unavailable.",
                        "model_loaded": False,
                    }
                ),
                503,
            )

    @app.route("/predict", methods=["POST"])
    def predict() -> tuple[Any, int]:
        if MODEL_BUNDLE is None:
            return jsonify({"error": "Model bundle is not available."}), 503

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a valid JSON object."}), 400

        feature_names = list(MODEL_BUNDLE.get("feature_names", []))
        if not feature_names:
            return jsonify({"error": "Model feature schema is missing."}), 500

        missing = [feature for feature in feature_names if feature not in payload]
        if missing:
            return jsonify({"error": "Missing required feature(s): " + ", ".join(missing)}), 400

        numeric_row = []
        for feature in feature_names:
            value = payload[feature]
            if value is None:
                return jsonify({"error": f"Feature '{feature}' cannot be null."}), 400
            try:
                numeric_row.append(float(value))
            except (TypeError, ValueError):
                return jsonify({"error": f"Feature '{feature}' must be numeric."}), 400

        input_frame = pd.DataFrame([numeric_row], columns=feature_names)
        pipeline = MODEL_BUNDLE["pipeline"]
        prediction = pipeline.predict(input_frame)[0]
        response: dict[str, Any] = {
            "status": "ok",
            "prediction": int(prediction),
            "label": "fraud" if int(prediction) == 1 else "non_fraud",
            "input_features": {k: safe_scalar(v) for k, v in payload.items() if k in feature_names},
        }

        if hasattr(pipeline, "predict_proba"):
            probability = pipeline.predict_proba(input_frame)[0, 1]
            response["probability"] = float(safe_scalar(probability))

        return jsonify(response), 200

    return app


def safe_scalar(value: Any) -> Any:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return [safe_scalar(v) for v in value.tolist()]
    return value


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
