# Fraud Detection Experiment Summary

## Objective
This experiment evaluates reproducible fraud-detection models on the real credit-card fraud dataset provided in the workspace.

## Dataset
- Source: ULB credit-card fraud dataset from the research paper reference
- Records: 284807
- Target: Class (0 = legitimate, 1 = fraud)
- Positive rate: 0.17%
- Train/test split: 80/20 with stratification and random seed 42

## Model comparison
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| xgboost | 0.9995 | 0.8804 | 0.8265 | 0.8526 | 0.9782 | 0.8745 |
| random_forest | 0.9991 | 0.7094 | 0.8469 | 0.7721 | 0.9821 | 0.8486 |
| logistic_regression | 0.9755 | 0.0610 | 0.9184 | 0.1144 | 0.9721 | 0.7189 |

## Best model selected
The best model by F1-score is **xgboost** with an F1-score of **0.8526**. This selection is based on the test set and not on training performance only.

## Notes
- The dataset is extremely imbalanced, so we prioritize precision/recall/F1 and PR-AUC in addition to ROC-AUC.
- The original paper focuses on AUC and runtime efficiency for CVQBoost versus XGBoost; this project emphasizes a reproducible, deployable model artifact and fair evaluation on held-out data.