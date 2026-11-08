# \# 🛡️ Network Intrusion Detection \& Anomaly Scoring System

# 

# <p align="center">

# &#x20; \*\*An ML-based network traffic anomaly detection system using Isolation Forest, PCA reconstruction error, and supervised Random Forest benchmarking.\*\*

# </p>

# 

# <p align="center">

# &#x20; !\[Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)

# &#x20; !\[Machine Learning](https://img.shields.io/badge/Machine%20Learning-Anomaly%20Detection-orange)

# &#x20; !\[Dataset](https://img.shields.io/badge/Dataset-CIC--IDS2017-green)

# &#x20; !\[Framework](https://img.shields.io/badge/Framework-Scikit--learn-F7931E?logo=scikitlearn)

# &#x20; !\[Interface](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)

# &#x20; !\[License](https://img.shields.io/badge/License-MIT-yellow)

# </p>

# 

# \---

# 

# \## 📌 Table of Contents

# 

# 1\. \[Overview](#-overview)

# 2\. \[Key Features](#-key-features)

# 3\. \[Dataset](#-dataset)

# 4\. \[System Architecture](#-system-architecture)

# 5\. \[Machine Learning Methodology](#-machine-learning-methodology)

# 6\. \[Experimental Design](#-experimental-design)

# 7\. \[Model Interpretation](#-model-interpretation)

# 8\. \[Project Structure](#-project-structure)

# 9\. \[Installation](#-installation)

# 10\. \[Running the Project](#-running-the-project)

# 11\. \[Testing](#-testing)

# 12\. \[Limitations](#-limitations)

# 13\. \[Documentation](#-documentation)

# 

# \---

# 

# \## 🔍 Overview

# 

# Network Intrusion Detection \& Anomaly Scoring System is a machine learning portfolio project designed to identify unusual patterns in network traffic flows.

# 

# The project uses genuine \*\*CIC-IDS2017 network-flow data\*\* and implements an unsupervised anomaly detection pipeline.

# 

# The primary detection model is \*\*Isolation Forest\*\*, trained exclusively on benign network traffic. PCA reconstruction error provides an additional unsupervised baseline, while Random Forest serves as a separate supervised reference model.

# 

# The objective is to explore how machine learning techniques can identify suspicious network behavior without treating anomaly scores as calibrated attack probabilities.

# 

# \### 🎯 Project Objectives

# 

# \- Build a reproducible network traffic preprocessing pipeline.

# \- Train an anomaly detector using benign traffic only.

# \- Compare Isolation Forest with PCA reconstruction error.

# \- Establish a separate supervised Random Forest reference.

# \- Select detection thresholds using validation data.

# \- Evaluate performance on later capture days.

# \- Generate interpretable diagnostic information and risk scores.

# 

# \---

# 

# \## ✨ Key Features

# 

# | Feature | Description |

# |---|---|

# | Network Traffic Analysis | Processes genuine CIC-IDS2017 flow records. |

# | Data Integrity | Records SHA-256 hashes of original CSV files. |

# | Data Preprocessing | Cleans columns and handles numeric values. |

# | Benign-Only Training | Fits imputation, scaling and unsupervised models on Monday BENIGN traffic only. |

# | Isolation Forest | Primary unsupervised anomaly detector. |

# | PCA Baseline | Uses reconstruction error to identify unusual observations. |

# | Random Forest | Separate supervised reference model. |

# | Threshold Selection | Uses Tuesday BENIGN validation scores. |

# | Risk Scoring | Converts anomaly scores into risk-oriented outputs. |

# | Explainability | Provides diagnostic feature deviation information. |

# | Streamlit Interface | Provides an application interface for the project. |

# 

# \---

# 

# \## 📊 Dataset

# 

# \*\*CIC-IDS2017 — Canadian Institute for Cybersecurity\*\*

# 

# Official dataset: https://www.unb.ca/cic/datasets/ids-2017.html

# 

# CIC-IDS2017 contains labeled network traffic flows captured across multiple weekdays and includes benign and attack traffic.

# 

# \### Dataset Setup

# 

# Download the original weekday CSV files from the official dataset source.

# 

# Place them inside:

# 

# ```text

# data/

# └── raw/

# &#x20;   ├── Monday-WorkingHours.pcap\_ISCX.csv

# &#x20;   ├── Tuesday-WorkingHours.pcap\_ISCX.csv

# &#x20;   ├── Wednesday-workingHours.pcap\_ISCX.csv

# &#x20;   ├── Thursday-WorkingHours-Morning-WebAttacks.pcap\_ISCX.csv

# &#x20;   ├── Thursday-WorkingHours-Afternoon-Infilteration.pcap\_ISCX.csv

# &#x20;   ├── Friday-WorkingHours-Morning.pcap\_ISCX.csv

# &#x20;   ├── Friday-WorkingHours-Afternoon-PortScan.pcap\_ISCX.csv

# &#x20;   └── Friday-WorkingHours-Afternoon-DDos.pcap\_ISCX.csv

# ```

# 

# \*Use the exact filenames from your downloaded dataset and the configuration expected by the project.\*

# 

# \*\*Important:\*\* Training stops if the required original dataset files are missing. Synthetic data is used exclusively for unit tests, not for reporting model performance.

# 

# \---

# 

# \## 🏗️ System Architecture

# 

# The project follows a modular machine learning pipeline.

# 

# ```mermaid

# flowchart TD

# &#x20;   A\["CIC-IDS2017 Raw CSV Files"] --> B\["Data Loading \& SHA-256 Recording"]

# &#x20;   B --> C\["Data Cleaning \& Feature Selection"]

# &#x20;   C --> D\["Monday BENIGN Training Data"]

# &#x20;   D --> E\["Median Imputation \& Scaling"]

# &#x20;   E --> F\["Isolation Forest"]

# &#x20;   E --> G\["PCA Reconstruction Baseline"]

# &#x20;   F --> H\["Tuesday BENIGN Threshold Selection"]

# &#x20;   G --> H

# &#x20;   H --> I\["Frozen Detection Threshold"]

# &#x20;   I --> J\["Wednesday–Friday Evaluation"]

# &#x20;   J --> K\["Evaluation \& Error Analysis"]

# &#x20;   K --> L\["Risk Scoring \& Streamlit Interface"]

# ```

# 

# \---

# 

# \## 🧠 Machine Learning Methodology

# 

# The project implements three distinct machine learning approaches.

# 

# \### 1. Isolation Forest — Primary Model

# 

# Isolation Forest is the primary unsupervised anomaly detection algorithm.

# 

# \*\*Training methodology:\*\*

# \- Uses Monday BENIGN network traffic.

# \- Learns patterns associated with benign network activity.

# \- Assigns anomaly scores to network flows.

# \- Uses a separately selected threshold to classify unusual observations.

# 

# The model does not require attack labels during its benign-only training stage.

# 

# \### 2. PCA Reconstruction Error — Unsupervised Baseline

# 

# Principal Component Analysis is used as an additional unsupervised baseline.

# 

# The approach:

# 1\. Learns a lower-dimensional representation of benign network traffic.

# 2\. Reconstructs observations from the reduced representation.

# 3\. Calculates reconstruction error.

# 4\. Uses reconstruction error as an indicator of unusual traffic.

# 

# Higher reconstruction error can indicate observations that differ from learned benign patterns.

# 

# \### 3. Random Forest — Supervised Reference

# 

# Random Forest is trained separately using labeled Monday and Tuesday data.

# 

# Its purpose is to provide a supervised reference for comparison.

# 

# \*\*Important distinction:\*\* Random Forest is not a benign-only anomaly detector. Its training methodology is separate from the Isolation Forest and PCA pipelines.

# 

# \---

# 

# \## 🧪 Experimental Design

# 

# A chronological, day-based experimental split is used.

# 

# | Dataset Partition | Purpose |

# |---|---|

# | Monday BENIGN | Fit imputation, scaling, Isolation Forest and PCA |

# | Tuesday BENIGN | Select detection thresholds |

# | Monday + Tuesday labeled data | Train separate supervised Random Forest reference |

# | Wednesday–Friday | Final evaluation of the frozen unsupervised detection pipeline |

# 

# \### Data Leakage Prevention

# 

# The following controls are implemented:

# 

# \- Median imputation is fitted only on Monday BENIGN training data.

# \- Scaling is fitted only on Monday BENIGN training data.

# \- Unsupervised models are trained only on Monday BENIGN traffic.

# \- Detection thresholds are selected using Tuesday BENIGN scores.

# \- Thresholds are frozen before final evaluation.

# \- Wednesday–Friday evaluation data is not used to fit preprocessing or select thresholds.

# 

# \### Feature Selection

# 

# The preprocessing pipeline excludes:

# 

# \- Identifiers

# \- Timestamp

# \- Destination port

# \- Target labels

# 

# This prevents these fields from being used as direct model inputs.

# 

# \---

# 

# \## 🔬 Model Interpretation

# 

# The project provides diagnostic information to help understand unusual network observations.

# 

# \### Anomaly Scores

# 

# Isolation Forest ranks network flows based on how unusual they are relative to learned benign patterns.

# 

# PCA reconstruction error provides a second anomaly-oriented signal.

# 

# \### Risk Scoring

# 

# Risk scoring provides a risk-oriented representation of model outputs.

# 

# \*\*Important:\*\* Anomaly scores are not calibrated attack probabilities.

# 

# \### Feature Deviation Explanations

# 

# Feature deviation information is used for diagnostic interpretation.

# 

# These explanations are not causal explanations and are not SHAP values.

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```text

# network-intrusion-detection-anomaly-scoring/

# │

# ├── app/

# │   └── streamlit\_app.py

# │

# ├── configs/

# │   └── config.yaml

# │

# ├── data/

# │   ├── raw/

# │   └── processed/

# │

# ├── docs/

# │   └── INTERVIEW\_GUIDE.md

# │

# ├── models/

# │

# ├── notebooks/

# │   └── 01\_network\_traffic\_eda.ipynb

# │

# ├── reports/

# │   ├── figures/

# │   ├── model\_card.md

# │   └── error\_analysis.md

# │

# ├── src/

# │   ├── \_\_init\_\_.py

# │   └── nids/

# │       ├── \_\_init\_\_.py

# │       ├── config.py

# │       ├── data\_loader.py

# │       ├── preprocessing.py

# │       ├── split.py

# │       ├── models.py

# │       ├── train.py

# │       ├── evaluate.py

# │       ├── threshold.py

# │       ├── risk\_scoring.py

# │       ├── explainability.py

# │       └── predict.py

# │

# ├── tests/

# │   ├── conftest.py

# │   ├── test\_data\_loader.py

# │   ├── test\_preprocessing.py

# │   ├── test\_split.py

# │   ├── test\_models.py

# │   ├── test\_risk\_scoring.py

# │   └── test\_prediction.py

# │

# ├── .gitignore

# ├── LICENSE

# ├── PROGRESS.md

# ├── README.md

# ├── requirements.txt

# └── RUN\_GUIDE.md

# ```

# 

# \---

# 

# \## ⚙️ Installation

# 

# \### Prerequisites

# 

# \- Python

# \- Git

# \- pip

# \- CIC-IDS2017 dataset

# 

# \### 1. Clone the repository

# 

# ```bash

# git clone https://github.com/yash-2999/network-intrusion-detection-anomaly-scoring.git

# ```

# 

# \### 2. Navigate to the project

# 

# ```bash

# cd network-intrusion-detection-anomaly-scoring

# ```

# 

# \### 3. Create a virtual environment

# 

# Windows PowerShell:

# 

# ```powershell

# python -m venv .venv

# ```

# 

# \### 4. Activate the environment

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

# 

# \### 5. Install dependencies

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# \### 6. Download the dataset

# 

# Download CIC-IDS2017 from its official source and place the original weekday CSV files inside `data/raw/`.

# 

# \---

# 

# \## 🚀 Running the Project

# 

# The exact execution sequence and configuration details are documented in:

# 

# \*\*\[RUN\_GUIDE.md](RUN\_GUIDE.md)\*\*

# 

# The Streamlit interface is located at:

# 

# ```text

# app/streamlit\_app.py

# ```

# 

# Launch it using the command specified in `RUN\_GUIDE.md`.

# 

# \---

# 

# \## 🧪 Testing

# 

# The project includes unit tests for important pipeline components.

# 

# Test coverage includes:

# 

# \- Data loading

# \- Preprocessing

# \- Dataset splitting

# \- Model behavior

# \- Risk scoring

# \- Prediction

# 

# Run the tests:

# 

# ```bash

# pytest -v

# ```

# 

# Synthetic data is used for unit testing so that tests do not depend on the full CIC-IDS2017 dataset.

# 

# \---

# 

# \## ⚠️ Limitations

# 

# This project is an educational batch-flow machine learning prototype, not a production intrusion detection system.

# 

# Known limitations include:

# 

# 1\. \*\*Dataset representativeness:\*\* CIC-IDS2017 may not represent modern production network traffic.

# 2\. \*\*Capture limitations:\*\* Dataset collection and capture conditions can influence model behavior.

# 3\. \*\*Day-based split limitations:\*\* Chronological day-based partitions do not guarantee statistical independence.

# 4\. \*\*False positives:\*\* Unusual benign traffic may be flagged as anomalous.

# 5\. \*\*False negatives:\*\* Some malicious traffic may resemble benign traffic.

# 6\. \*\*Score calibration:\*\* Anomaly scores must not be interpreted as calibrated attack probabilities.

# 7\. \*\*Human review:\*\* Detection results require further investigation and human judgment.

# 

# \---

# 

# \## 📚 Documentation

# 

# Additional project documentation:

# 

# \- \[Interview Preparation Guide](docs/INTERVIEW\_GUIDE.md)

# \- \[Model Card](reports/model\_card.md)

# \- \[Error Analysis](reports/error\_analysis.md)

# \- \[Execution Guide](RUN\_GUIDE.md)

# \- \[Project Progress](PROGRESS.md)

# 

# \---

# 

# \## 🤝 Contributing

# 

# Contributions and suggestions are welcome.

# 

# 1\. Fork the repository.

# 2\. Create a feature branch.

# 3\. Implement your changes.

# 4\. Add or update tests.

# 5\. Submit a pull request.

# 

# \---

# 

# \## 📄 License

# 

# This project is distributed under the MIT License.

# 

# See \[LICENSE](LICENSE) for more information.

# 

# \---

# 

# <p align="center">

# &#x20; \*\*Built as an educational machine learning and network security portfolio project.\*\*

# </p>

# 

# <p align="center">

# &#x20; ⭐ If you find this project useful, consider starring the repository.

# </p>

