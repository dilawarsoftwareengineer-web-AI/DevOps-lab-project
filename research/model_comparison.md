# Model Comparison

The real dataset in this project is a highly imbalanced credit-card fraud dataset. The target variable is `Class`, where `0` indicates legitimate transactions and `1` indicates fraudulent ones.

## Experimental setup

- Dataset: `creditcard.csv`
- Rows: 284,807
- Features: `Time`, `V1`–`V28`, `Amount`
- Target: `Class`
- Split: 80/20 stratified train/test split with random seed 42
- Primary metric for model selection: F1-score on the held-out test set
- Secondary metrics: precision, recall, ROC-AUC, PR-AUC, confusion matrix

## Results from the actual training run

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XGBoost | 0.9995 | 0.8804 | 0.8265 | 0.8526 | 0.9782 | 0.8745 |
| Random Forest | 0.9991 | 0.7094 | 0.8469 | 0.7721 | 0.9821 | 0.8486 |
| Logistic Regression | 0.9755 | 0.0610 | 0.9184 | 0.1144 | 0.9721 | 0.7189 |

## Interpretation

The XGBoost model performed best on the held-out test data by F1-score, which is a more meaningful measure than raw accuracy in this imbalanced context. While the logistic regression model achieves a high recall, it produces many false positives and is therefore not competitive on precision-oriented fraud detection.

The random forest model performs reasonably well but is not as strong as XGBoost in the chosen metric. The selected best model is therefore the XGBoost pipeline saved in the model bundle.

## Comparison with the paper

The paper reports AUC-focused comparisons with CVQBoost and XGBoost. This project evaluates a reproducible classical benchmark using the same underlying fraud-detection task, with classical metrics suited to real-world deployment and an explicit artifact export. The goal here is not to claim a superior optimization algorithm but to build an audit trail that can be reproduced locally and through CI.
