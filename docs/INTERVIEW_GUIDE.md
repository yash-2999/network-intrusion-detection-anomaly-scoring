# Interview Guide

## Project summary
A CIC-IDS2017 flow classifier/anomaly-scoring prototype. Isolation Forest learns a benign profile from Monday BENIGN flows. PCA reconstruction error is an unsupervised baseline. Random Forest is a separately trained supervised reference using labeled Monday+Tuesday rows; it is not part of the benign-only fitting protocol. Tuesday BENIGN validation scores set an FPR-based threshold; Wednesday-Friday are held out for test.

## Concepts
- Isolation Forest: random partitioning isolates rare/unusual points in fewer splits.
- PCA reconstruction: compress and reconstruct benign data; large mean squared reconstruction error indicates deviation.
- Anomaly score: relative unusualness, not attack probability.
- Supervised vs unsupervised: Random Forest learns labels; anomaly detectors fit benign-only traffic.
- Precision = TP/(TP+FP); recall = TP/(TP+FN).
- ROC-AUC measures ranking over thresholds; PR-AUC is useful under imbalance and must be compared with attack prevalence.
- False positive: benign flow flagged. False negative: attack missed.
- Leakage: fitting preprocessing or tuning on held-out data. Fit imputer/scaler on training only.
- Threshold: selected from validation benign score quantiles to target FPR, then frozen before test.

## 15 interview questions
1. Why Isolation Forest? It detects rare deviations without attack labels for fitting.
2. Why benign-only? It models expected benign behavior.
3. Why Random Forest? A supervised reference, not the same learning setup.
4. Why PCA? Independent reconstruction-based baseline.
5. Is anomaly score probability? No, it is an uncalibrated score.
6. Why not accuracy alone? Class imbalance can hide missed attacks.
7. Define precision. Share of alerts that are true attacks.
8. Define recall. Share of attacks detected.
9. Why PR-AUC? It highlights positive-class performance under imbalance.
10. Define FPR. FP divided by all actual benign flows.
11. Why day split? Reduces random mixing across capture days but cannot ensure independence.
12. Why train-only scaling? Avoids leakage from validation/test distributions.
13. How threshold chosen? Validation BENIGN quantiles at target FPR.
14. Key limitations? Dataset age, day shift, alert burden, no live traffic.
15. Production-ready? No; educational prototype requiring operational validation.
