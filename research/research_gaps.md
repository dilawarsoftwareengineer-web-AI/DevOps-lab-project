# Research Gaps and Limitations

## 1. Limitations explicitly reported in the paper

The provided paper is explicit that it is a performance and scalability study for CVQBoost rather than a deployment-focused benchmark. The paper’s main claims are dominated by runtime and AUC comparisons, not by production inference or business deployment concerns. As a result, the following limitations remain:

- The paper does not provide a packaged inference API or deployment-oriented model artifact.
- The work focuses on optimization speed and scaling rather than practical production monitoring.
- The paper evaluates algorithmic performance under a benchmark framing, not a full fraud-operations lifecycle with drift monitoring, retraining, and governance.

## 2. Gaps supported by the reviewed literature

The literature on imbalanced fraud detection recognizes several practical issues that are not fully addressed by a single benchmark study:

- Class imbalance can substantially distort model choice if accuracy is used as the sole metric.
- Fraud detection systems must often balance precision and recall under severe cost asymmetry; a single aggregate score is not enough.
- Real-world fraud data often experiences concept drift, seasonal changes, and evolving adversarial behavior, which can reduce static-model performance over time.
- Feature engineering, transaction context, and out-of-distribution detection are often essential in production fraud systems, beyond tabular PCA-like transformed features alone.

## 3. Limitations demonstrated by our experiments

This project’s experiments show that:

- Accuracy is misleadingly high in a highly imbalanced problem; it can remain near 0.999 even when fraud detection quality is modest or uneven.
- A single model that has strong ROC-AUC is not necessarily best under precision/recall trade-offs.
- Logistic regression performs poorly under precision-centric evaluation in the default configuration and is therefore not a strong choice for the final artifact.
- The best-performing model in this benchmark is selected using F1-score on held-out data rather than by training accuracy, which is a more honest evaluation setup.

## 4. Future improvements that remain proposals

The following improvements are consistent with the evidence but were not adopted here as part of a tested claim:

- Use more advanced imbalance handling or cost-sensitive thresholds tuned to operational fraud costs.
- Add feature engineering informed by transaction metadata, merchant patterns, or time-based effects.
- Compare more tree-based models and transformer-based or semi-supervised approaches on the same task.
- Build a production monitoring pipeline with drift detection, alerting, and retraining.
- Evaluate the model under realistic temporal splits rather than a random split, which better reflects deployment conditions.

These are promising next steps, but they remain proposals unless they are tested with evidence.
