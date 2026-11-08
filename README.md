# Network Intrusion Detection & Anomaly Scoring System

Fresher-level portfolio project using genuine CIC-IDS2017 network-flow data. Isolation Forest is the primary benign-only anomaly detector; PCA reconstruction error is an unsupervised baseline; Random Forest is a separate supervised reference.

## Dataset
Download CIC-IDS2017 from https://www.unb.ca/cic/datasets/ids-2017.html and put the original weekday CSV files in `data/raw/`. Training stops if files are missing. Synthetic data is used only in unit tests. No dataset metrics are fabricated.

## Workflow
Load CSVs and record SHA-256; clean columns and numeric values; exclude identifiers, timestamp, destination port and labels; fit median imputation/scaling on Monday BENIGN only; train Isolation Forest and PCA on benign traffic; train Random Forest separately on labeled Monday+Tuesday data (a separate supervised reference partition); choose thresholds from Tuesday BENIGN scores; freeze threshold and evaluate Wednesday-Friday.

## Models and interpretation
Isolation Forest ranks unusual flows. PCA uses reconstruction error. Random Forest is supervised and not a benign-only detector. Scores are not calibrated attack probabilities. Deviation explanations are diagnostic, not causal or SHAP.

## Run
See RUN_GUIDE.md. This is an educational batch-flow prototype, not a production IDS. Day-based splits do not guarantee independence; CIC-IDS2017 has representativeness and capture limitations; false positives and false negatives require human review.
