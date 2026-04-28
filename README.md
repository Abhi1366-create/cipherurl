# CipherURL — Phishing URL Detection System

## Overview

CipherURL is a machine learning-based tool that classifies URLs as phishing or legitimate using an XGBoost model. The system analyzes URL patterns and provides a clear, explainable result.

---

## Demo

![App Screenshot](https://raw.githubusercontent.com/Abhi1366-create/cipherurl/main/Screenshot.png)

---

## Features

* URL-based phishing detection
* Numeric risk score
* Clear classification (Phishing / Safe)
* Explanation of results
* URL structure breakdown
* External reporting (Google Safe Browsing, PhishTank)

---

## Model Details

* Algorithm: XGBoost
* Dataset size: ~247,000 samples
* Features: 40+ engineered features
* Accuracy: ~93–95%
* Focus: reducing missed phishing attacks (high recall)

---

## How It Works

1. User enters a URL
2. Features are extracted from the URL
3. Model predicts phishing probability
4. Decision is made using a threshold
5. Result and explanation are displayed

---

## Project Structure

```
cipherurl/
├── app/
│   └── app.py
├── src/
│   └── train.py
├── requirements.txt
├── Screenshot.png
└── README.md
```

---

## Setup and Run

### Install dependencies

```
pip install -r requirements.txt
```

### Train the model

```
python src/train.py
```

### Run the application

```
streamlit run app/app.py
```

Note: You must train the model before running the app, as the model file is not included.

---

## Dataset

The dataset is not included in the repository due to size.

---

## Notes

* This project is for educational purposes
* Feature extraction in the UI is simplified
* Not intended for production use

---

## About the Developer

### Abhishek M R

BCA Student | AI & Cybersecurity Enthusiast
