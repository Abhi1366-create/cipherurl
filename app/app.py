import streamlit as st
import pickle
import pandas as pd
import urllib.parse
import os

MODEL_PATH = "models/model.pkl"

# check model exists
if not os.path.exists(MODEL_PATH):
    st.error("Model not found. Run: python src/train.py")
    st.stop()

# load model
with open(MODEL_PATH, "rb") as f:
    model, feature_names, threshold = pickle.load(f)

# feature extraction
def extract_features(url):
    url = url.lower()

    features = {}

    features['url_length'] = len(url)
    features['number_of_dots_in_url'] = url.count('.')
    features['number_of_digits_in_url'] = sum(c.isdigit() for c in url)
    features['number_of_hyphens_in_url'] = url.count('-')
    features['number_of_slash_in_url'] = url.count('/')
    features['number_of_questionmark_in_url'] = url.count('?')
    features['number_of_equal_in_url'] = url.count('=')
    features['number_of_at_in_url'] = url.count('@')

    try:
        domain = url.split('/')[2]
    except:
        domain = url

    features['domain_length'] = len(domain)
    features['number_of_dots_in_domain'] = domain.count('.')
    features['number_of_hyphens_in_domain'] = domain.count('-')
    features['having_digits_in_domain'] = int(any(c.isdigit() for c in domain))

    # fill missing features
    for f in feature_names:
        if f not in features:
            features[f] = 0

    return pd.DataFrame([features])[feature_names]

# UI
st.set_page_config(page_title="CipherURL", layout="centered")

st.title("CipherURL - Phishing URL Detector")

url = st.text_input("Enter URL")

if st.button("Analyze"):
    if not url:
        st.warning("Enter a URL")
    else:
        X = extract_features(url)

        prob = model.predict_proba(X)[0][1]
        prediction = 1 if prob >= threshold else 0

        label = "Phishing" if prediction == 1 else "Safe"
        confidence = prob if prediction == 1 else (1 - prob)

        st.subheader("Result")
        st.write(f"Classification: {label}")
        st.write(f"Confidence: {confidence * 100:.2f}%")

        st.subheader("Risk Score")
        risk = prob * 100
        st.write(f"{risk:.2f}%")
        st.progress(int(risk))

        st.subheader("URL Breakdown")

        domain = url.split('/')[2] if "://" in url else url

        st.write(f"Domain: {domain}")
        st.write(f"Length: {len(url)}")
        st.write(f"Subdomains: {domain.count('.')}")
        st.write(f"Contains digits: {'Yes' if any(c.isdigit() for c in url) else 'No'}")
        st.write(f"Contains @: {'Yes' if '@' in url else 'No'}")

        st.subheader("Explanation")

        reasons = []

        if len(url) > 75:
            reasons.append("URL is long")

        if domain.count('.') > 2:
            reasons.append("Many subdomains")

        if any(c.isdigit() for c in domain):
            reasons.append("Digits in domain")

        if '-' in domain:
            reasons.append("Hyphens in domain")

        if '@' in url:
            reasons.append("Contains @ symbol")

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("No strong indicators detected")

        st.subheader("Report")

        encoded_url = urllib.parse.quote(url)

        st.markdown(
            f"""
            - [Report to Google Safe Browsing](https://safebrowsing.google.com/safebrowsing/report_phish/?url={encoded_url})
            - [Submit to PhishTank](https://phishtank.org/submit.php)
            """
        )