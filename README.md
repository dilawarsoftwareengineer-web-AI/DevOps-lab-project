# Credit Card Fraud Detection DevOps Project

## Overview

This project uses the real credit-card fraud dataset provided in the workspace and the research paper `2503.11273v1 (1).pdf` to build a reproducible machine-learning workflow. The goal is to train and compare realistic fraud-detection models, save the best artifact, expose predictions through a Flask API, and present a public-facing Angular dashboard on GitHub Pages.

The underlying task is binary fraud detection on the ULB credit-card dataset, where the target is `Class` and the positive class (`1`) represents fraudulent transactions. Because the dataset is highly imbalanced, the project prioritizes precision, recall, F1-score, and PR-AUC instead of relying on raw accuracy alone.

## Research paper and dataset

- Paper: `2503.11273v1 (1).pdf`
- Dataset: `creditcard.csv`
- Verified dataset shape: 284,807 rows x 31 columns
- Target variable: `Class`
- Fraud rate: 0.17%
- Missing values: none detected
- Duplicate rows: 1,081 exact duplicates

The paper focuses on comparing CVQBoost and XGBoost for fraud detection while emphasizing runtime and scaling. This project adopts the same underlying problem but prioritizes reproducible evaluation, saved artifacts, and deployment workflow using Python, Flask, Angular, and GitHub Actions.

## Training and evaluation procedure

The training workflow is implemented in `backend/train_model.py`.

- Data is loaded from `creditcard.csv`.
- The target column is separated from the feature columns.
- A stratified 80/20 train/test split is used with random seed 42.
- The following models are trained and compared:
  - Logistic Regression
  - Random Forest
  - XGBoost
- The best model is chosen using F1-score on the held-out test set.
- All results are exported to:
  - `results/model_comparison.csv`
  - `results/metrics.json`
  - `results/experiment_summary.md`

## Actual model comparison results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XGBoost | 0.9995 | 0.8804 | 0.8265 | 0.8526 | 0.9782 | 0.8745 |
| Random Forest | 0.9991 | 0.7094 | 0.8469 | 0.7721 | 0.9821 | 0.8486 |
| Logistic Regression | 0.9755 | 0.0610 | 0.9184 | 0.1144 | 0.9721 | 0.7189 |

Selected model: XGBoost

## Model artifact and feature schema

The final trained bundle is saved in:

- `backend/models/model_bundle.joblib`
- `backend/models/model_bundle.pkl`

The bundle contains:

- the fitted XGBoost pipeline
- exact feature names and order
- target metadata
- model version
- package versions
- evaluation metrics

## Research gaps and limitations

This project documents the actual limitations and gaps in:

- `research/research_gaps.md`
- `research/model_comparison.md`
- `research/related_work.md`

The public-facing project is a dashboard and research summary, not a claim of a new algorithmic breakthrough. The static site cannot execute the Flask model or Python code itself.

## Flask API

The Flask backend is implemented in `backend/app.py`.

Endpoints:

- `GET /health` — returns API status and model metadata
- `POST /predict` — validates JSON input and returns the prediction, label, and probability if supported

Requirements are listed in `backend/requirements.txt`.

## Angular frontend

The Angular frontend is built in the root-level `src/` application with project configuration at the repository root.

Features:

- overview and project narrative
- dataset summary and real model metrics
- feature-driven prediction form matching the model schema
- loading, success, and error states
- disclaimer that live prediction requires a running Flask backend locally

Development proxy:

- `proxy.conf.json` forwards `/api` requests to `http://127.0.0.1:5000`

## Local setup (Windows)

1. Create and activate a virtual environment if desired.
2. Install Python dependencies:
   ```powershell
   python -m pip install -r backend/requirements.txt
   ```
3. Train the model:
   ```powershell
   python backend/train_model.py
   ```
4. Start the Flask API:
   ```powershell
   python -m flask --app backend.app run --host 127.0.0.1 --port 5000
   ```
5. Install Node dependencies:
   ```powershell
   npm install
   ```
6. Start the Angular app:
   ```powershell
   npx -p node@22.22.3 ng serve --proxy-config proxy.conf.json --host 0.0.0.0 --port 4200
   ```
7. Open:
   - Flask: http://127.0.0.1:5000
   - Angular: http://localhost:4200

## Test commands

```powershell
python -m pytest backend/tests -q
```

```powershell
npx -p node@22.22.3 ng build --configuration production --base-href /DevOps-lab-project/
```

## GitHub Actions CI/CD

The repository includes GitHub Actions workflows for:

- Python backend validation and pytest execution
- Angular production build validation
- GitHub Pages deployment

Files:

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`

## GitHub repository and deployment URLs

GitHub repository:

- https://github.com/dilawarsoftwareengineer-web-AI/DevOps-lab-project

GitHub Pages URL:

- https://dilawarsoftwareengineer-web-AI.github.io/DevOps-lab-project/

## Public deployment limitations

GitHub Pages only hosts static content. It cannot run Python or access the saved model bundle. The public site therefore:

- presents the research summary and dashboard
- displays genuine saved model comparison results from the published assets
- clearly explains that live inference requires a local or hosted Flask API
- does not claim that the site itself makes predictions without a backend

## Research disclaimer

This project is built on the provided paper and dataset. The work documents real experimental results and reproducible pipeline artifacts and should be interpreted as a benchmark and deployment exercise rather than a claim of an original algorithmic improvement beyond the underlying research context.
