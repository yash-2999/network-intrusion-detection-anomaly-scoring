# Windows PowerShell Run Guide

## Extract and open
Extract the ZIP. In VS Code use File → Open Folder and select the project root (the folder containing README.md, requirements.txt, app, src and data).

## Environment
Use Python 3.10–3.12 (recommended 3.11):
```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Install packages:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import pandas, sklearn, streamlit; print('Dependencies OK')"
```

## Dataset
Download original CIC-IDS2017 CSVs from https://www.unb.ca/cic/datasets/ids-2017.html. Place them in `data/raw/`; preserve weekday text in filenames. The day split requires Monday, Tuesday, and Wednesday–Friday files. Missing data causes an explicit error, not synthetic training.

## First run (from project root)
```powershell
python -m pytest -q
python -m src.nids.train
python -m src.nids.evaluate
python -m streamlit run app/streamlit_app.py
```
Training writes model artifacts under `models/` and `reports/training_summary.json`. Evaluation writes `reports/metrics.json`. Streamlit opens at http://localhost:8501. Stop with Ctrl+C.

## Dashboard
Overview shows training summary; Model Performance shows held-out metrics; Anomaly Detection accepts a compatible flow CSV and provides downloadable scores; Risk Scoring explains risk bands; PCA Visualization displays explained variance. Upload CSVs with the same numeric feature schema used during training.

## Reopen later without retraining
```powershell
cd "C:\PATH\TO\network-intrusion-detection-anomaly-scoring"
.\.venv\Scripts\Activate.ps1
python -m streamlit run app/streamlit_app.py
```
Do not retrain if the model artifacts remain present and the feature schema is unchanged.

## Troubleshooting
- Python not recognized: install Python 3.11 and enable Add to PATH.
- Activation blocked: use the process-scoped policy command above.
- ModuleNotFoundError: activate `.venv`, then `pip install -r requirements.txt`.
- Dataset not found: verify original CSVs are inside `data/raw/` and filenames include weekdays.
- Memory error: this implementation concatenates chunks in memory; use a machine with adequate RAM or implement an out-of-core extension.
- Model missing: train after dataset setup.
- Streamlit missing: `python -m pip install streamlit`.
- Port busy: `python -m streamlit run app/streamlit_app.py --server.port 8502`.
- Missing CSV columns: use the CIC feature schema that matches the training metadata.
- Package issues: use Python 3.10–3.12 in a fresh virtual environment.

## Verification
```powershell
python --version
python -m pip check
Get-ChildItem .\data\raw\*.csv
Get-ChildItem .\models\
python -m pytest -q
python -c "from src.nids.predict import load_artifacts; print(load_artifacts().keys())"
```
Model loading succeeds only after training. Capture screenshots of each dashboard page for your portfolio. In interviews, explain the benign-only training set, leakage prevention, validation FPR threshold, supervised baseline distinction, and false-positive trade-off.

## One-shot first-time sequence
```powershell
python --version
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -q
# Install real CIC-IDS2017 CSV files into data/raw/ before proceeding.
python -m src.nids.train
python -m src.nids.evaluate
python -m streamlit run app/streamlit_app.py
```
