# CipherURL — Phishing URL Detection System

## Overview
CipherURL is a machine learning-based tool that classifies URLs as phishing or legitimate. It is built using XGBoost and focuses on identifying patterns commonly found in malicious URLs.

The project emphasizes both detection performance and interpretability, making it suitable for demonstration and learning purposes in cybersecurity and applied machine learning.

---

## Features

- URL-based phishing detection
- Risk score visualization
- Explanation of predictions
- URL structure breakdown
- External reporting links:
  - Google Safe Browsing
  - PhishTank

---

## Model Details

- Algorithm: XGBoost (gradient boosting)
- Dataset size: ~247,000 samples
- Features: 40+ engineered URL features
- Accuracy: ~93–95%
- Focus: improving recall for phishing detection (reducing missed threats)

---

## How It Works

1. The user inputs a URL
2. The system extracts relevant features
3. The model predicts the probability of phishing
4. A decision is made using a tuned threshold
5. The result is displayed along with an explanation

---

## Project Structure
cipherurl/
│
├── data/
│ └── dataset.csv
│
├── models/
│ └── model.pkl
│
├── src/
│ └── train.py
│
├── app/
│ └── app.py
│
├── requirements.txt
└── README.md

---

## Setup and Run

### Install dependencies
pip install -r requirements.txt


### Train the model

python src/train.py


### Run the application

streamlit run app/app.py

---

## Notes

- This project is intended for educational use
- The feature extraction in the UI is a simplified approximation of the dataset features
- It is not intended for production security use

---

## Possible Improvements

- Full feature extraction pipeline from raw URLs
- Integration with threat intelligence APIs
- Model comparison (LightGBM, CatBoost)
- Deployment to cloud or web platforms

---

## About Me
Abhishek M R

BCA Student | AI & Cybersecurity Enthusiast