# Project Plan

## Phase 1 findings

### Dataset
- Source: creditcard.csv (provided in the workspace; the archive.zip contains the same file)
- Shape: 284,807 rows x 31 columns
- Target variable: Class
- Positive class (fraud): 492 rows (0.17%)
- Negative class (non-fraud): 284,315 rows (99.83%)
- Features: Time, V1-V28, Amount, Class
- Missing values: none observed
- Duplicate rows: 1,081 exact duplicates
- Data type profile: all predictors are numeric floats; Class is integer-coded binary
- Class imbalance: severe, so accuracy is a poor primary metric; precision/recall/F1/PR-AUC/ROC-AUC are more informative
- There are no obvious missing-value placeholders or non-numeric columns in the raw CSV; feature leakage risk is low if the target column is excluded before training and if no imputation or encoding is applied using the whole dataset outside train/test splitting

### Research paper
- File: 2503.11273v1 (1).pdf
- Title: "Financial Fraud Detection with Entropy Computing"
- Objective: compare a novel optimizer called CVQBoost (implemented on Quantum Computing Inc.'s Dirac-3 hardware) to XGBoost for fraud detection on the ULB credit-card dataset
- Evaluation focus: Area under the ROC curve (AUC), with runtime comparisons across synthetic and real dataset scales
- Methodological emphasis: hardware acceleration, optimization behavior, and scaling with feature count and dataset size
- Key result reported in the paper: CVQBoost maintains competitive AUC values while showing much faster training times than conventional XGBoost implementations
- Paper context: the work is primarily a high-performance-computing and optimization paper, not a production-ready ML deployment project

### Repository state
- The current workspace is not initialized as a Git repository.
- There is no remote configured yet.
- No project scaffold, backend, frontend, or CI workflow exists in the workspace initially.

### Missing information / risk areas
- The paper does not provide a deployable API or production-ready model bundle.
- No codebase, environment lockfile, saved artifact, or model metadata existed before this work started.
- The research paper is a runtime-and-optimization study; it does not define a production-facing inference schema or front-end interface.
- The workspace contains the same dataset and paper only; we must build the reproducible ML pipeline, API, frontend, and deployment workflow from scratch while preserving the original artifacts.

## Phase 2 and later plan

This project will use the real dataset to train a reproducible fraud-detection pipeline, evaluate multiple classical baselines and a suitable boosting approach, compare results against the paper, save the best model artifact, expose it through a Flask API, and deliver an Angular frontend plus GitHub Pages deployment via Actions.

The project will keep the original paper and dataset intact, add the ML training workflow under the workspace, and record actual results only.
