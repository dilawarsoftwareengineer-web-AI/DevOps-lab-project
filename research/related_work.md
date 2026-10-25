# Related Work

This project is grounded in the actual dataset and research paper present in the workspace: the credit-card fraud detection study that compares CVQBoost with XGBoost for fraud detection under an imbalanced classification setting.

## Relevant literature and context

- The underlying dataset is the ULB credit-card fraud detection dataset described by the Kaggle repository referenced in the paper.
- The paper frames the task as a fraud-classification problem using a highly imbalanced binary target (`Class` = 0/1).
- XGBoost is used as the conventional baseline because it is a well-established gradient-boosted tree method that is widely adopted for tabular classification and is directly benchmarked against CVQBoost in the paper.
- The paper also discusses the use of imbalanced-learning strategies such as ADASYN, SMOTE, SVMSMOTE, and downsampling to adjust class ratios during training.
- This project does not claim an independent research contribution beyond reproducing a realistic benchmark workflow with the provided real dataset, evaluating several relevant baselines, and packaging a deployable model for inference.

## Direct alignment with the provided paper

The selected model and evaluation procedure are aligned with the fraud-detection setting described in the paper, with one important distinction: the project emphasizes a reproducible, production-ready evaluation workflow and artifact export rather than a hardware-optimization benchmark alone.

In this workflow:

- The real dataset is used without inventing alternative data sources.
- The target is the binary `Class` indicator.
- Model training and evaluation are performed on held-out data to avoid optimistic bias.
- Strong class imbalance is handled explicitly through appropriate metrics and a realistic train/test split.

## Research position

This project complements the original paper by operationalizing the same fraud-detection task in a reproducible ML pipeline, exposing the resulting model through a Flask API and Angular UI. It does not claim novelty in the optimization method itself; instead, it validates a benchmark workflow grounded in the available evidence.
