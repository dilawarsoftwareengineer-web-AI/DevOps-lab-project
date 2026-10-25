from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

DATA_PATH = Path(__file__).resolve().parents[1] / "creditcard.csv"
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
MODELS_DIR = Path(__file__).resolve().parent / "models"
SEED = 42


@dataclass
class ModelCandidate:
    name: str
    estimator: Any


def make_pipeline(name: str, est: Any) -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[("num", numeric_transformer, list(df_columns()))],
        remainder="drop",
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", est)])


def df_columns() -> list[str]:
    df = pd.read_csv(DATA_PATH)
    return [col for col in df.columns if col != "Class"]


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_PATH)
    if "Class" not in df.columns:
        raise ValueError("Target column 'Class' not found.")
    X = df.drop(columns=["Class"])
    y = df["Class"].astype(int)
    return X, y


def build_model_candidates() -> list[ModelCandidate]:
    return [
        ModelCandidate(
            "logistic_regression",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                solver="liblinear",
                random_state=SEED,
            ),
        ),
        ModelCandidate(
            "random_forest",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_leaf=3,
                class_weight="balanced",
                random_state=SEED,
            ),
        ),
        ModelCandidate(
            "xgboost",
            XGBClassifier(
                objective="binary:logistic",
                eval_metric="logloss",
                n_estimators=400,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                min_child_weight=1,
                scale_pos_weight=578,
                random_state=SEED,
                n_jobs=4,
            ),
        ),
    ]


def evaluate_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, Any]:
    proba = model.predict_proba(X_test)[:, 1]
    pred = model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "pr_auc": float(average_precision_score(y_test, proba)),
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
    }
    return metrics


def train_and_compare() -> pd.DataFrame:
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )

    results = []
    trained = {}
    for candidate in build_model_candidates():
        model = make_pipeline(candidate.name, clone(candidate.estimator))
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        metrics["model_name"] = candidate.name
        metrics["n_train"] = len(X_train)
        metrics["n_test"] = len(X_test)
        results.append(metrics)
        trained[candidate.name] = model

    comparison = pd.DataFrame(results)
    comparison = comparison.sort_values("f1", ascending=False, kind="mergesort").reset_index(drop=True)
    return comparison, trained, X_train, X_test, y_train, y_test


def save_results(comparison: pd.DataFrame) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "random_seed": SEED,
        "target": "Class",
        "dataset_file": str(DATA_PATH.name),
        "rows": int(len(pd.read_csv(DATA_PATH))),
        "columns": list(pd.read_csv(DATA_PATH).columns),
        "models": [
            {
                "model_name": row["model_name"],
                "accuracy": row["accuracy"],
                "precision": row["precision"],
                "recall": row["recall"],
                "f1": row["f1"],
                "roc_auc": row["roc_auc"],
                "pr_auc": row["pr_auc"],
            }
            for _, row in comparison.iterrows()
        ],
    }
    with (RESULTS_DIR / "metrics.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def write_experiment_summary(comparison: pd.DataFrame) -> None:
    summary_path = RESULTS_DIR / "experiment_summary.md"
    best = comparison.iloc[0]
    rows = [
        "# Fraud Detection Experiment Summary",
        "",
        "## Objective",
        "This experiment evaluates reproducible fraud-detection models on the real credit-card fraud dataset provided in the workspace.",
        "",
        "## Dataset",
        "- Source: ULB credit-card fraud dataset from the research paper reference",
        f"- Records: {int(len(pd.read_csv(DATA_PATH)))}",
        "- Target: Class (0 = legitimate, 1 = fraud)",
        "- Positive rate: 0.17%",
        "- Train/test split: 80/20 with stratification and random seed 42",
        "",
        "## Model comparison",
        "| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for _, row in comparison.iterrows():
        rows.append(
            f"| {row['model_name']} | {row['accuracy']:.4f} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1']:.4f} | {row['roc_auc']:.4f} | {row['pr_auc']:.4f} |"
        )

    rows.extend(
        [
            "",
            "## Best model selected",
            f"The best model by F1-score is **{best['model_name']}** with an F1-score of **{best['f1']:.4f}**. This selection is based on the test set and not on training performance only.",
            "",
            "## Notes",
            "- The dataset is extremely imbalanced, so we prioritize precision/recall/F1 and PR-AUC in addition to ROC-AUC.",
            "- The original paper focuses on AUC and runtime efficiency for CVQBoost versus XGBoost; this project emphasizes a reproducible, deployable model artifact and fair evaluation on held-out data.",
        ]
    )
    summary_path.write_text("\n".join(rows), encoding="utf-8")


def save_model_bundle(best_model: Any, feature_names: list[str], metrics: dict[str, Any]) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    bundle = {
        "task": "binary_classification",
        "target": "Class",
        "target_values": {0: "non_fraud", 1: "fraud"},
        "model_name": best_model.named_steps["model"].__class__.__name__,
        "feature_names": feature_names,
        "model_version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "random_seed": SEED,
        "metrics": metrics,
        "package_versions": {
            "python": __import__("platform").python_version(),
            "pandas": __import__("pandas").__version__,
            "numpy": __import__("numpy").__version__,
            "scikit_learn": __import__("sklearn").__version__,
            "xgboost": __import__("xgboost").__version__,
            "flask": __import__("flask").__version__,
        },
        "pipeline": best_model,
    }
    joblib.dump(bundle, MODELS_DIR / "model_bundle.joblib")
    with (MODELS_DIR / "model_bundle.pkl").open("wb") as fh:
        pickle.dump(bundle, fh)


def main() -> None:
    comparison, trained, X_train, X_test, y_train, y_test = train_and_compare()
    save_results(comparison)
    write_experiment_summary(comparison)
    best_model_name = comparison.iloc[0]["model_name"]
    best_model = trained[best_model_name]
    feature_names = [col for col in X_train.columns]
    metrics = comparison.iloc[0].to_dict()
    save_model_bundle(best_model, feature_names, metrics)
    print("=== MODEL COMPARISON ===")
    print(comparison.to_string(index=False))
    print(f"\nSelected best model: {best_model_name}")
    print(f"Model artifact saved to: {MODELS_DIR / 'model_bundle.joblib'}")


if __name__ == "__main__":
    main()
