import streamlit as st
import pickle
import pandas as pd
import re
import urllib.parse

MODEL_PATH = "models/model.pkl"

# Load model
with open(MODEL_PATH, "rb") as f:
    model, feature_names, threshold = pickle.load(f)

# ─────────────────────────────
# FEATURE EXTRACTION (simplified)
# ─────────────────────────────
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

    # Fill missing features with 0
    for f in feature_names:
        if f not in features:
            features[f] = 0

    return pd.DataFrame([features])[feature_names]


# ─────────────────────────────
# UI
# ─────────────────────────────
st.set_page_config(page_title="CipherURL", layout="centered")

st.title("🔍 CipherURL - Phishing URL Detector")
st.write("Analyze URLs for potential phishing threats.")

url = st.text_input("Enter URL")

if st.button("Analyze"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        X = extract_features(url)

        prob = model.predict_proba(X)[0][1]
        prediction = 1 if prob >= threshold else 0

        st.markdown("---")

        # RESULT
        if prediction == 1:
            st.error(f"🚨 PHISHING DETECTED\nConfidence: {prob*100:.2f}%")
        else:
            st.success(f"✅ URL APPEARS SAFE\nConfidence: {(1-prob)*100:.2f}%")

        # ─────────────
        # RISK SCORE
        # ─────────────
        st.subheader("Risk Score")
        st.progress(int(prob * 100))

        # ─────────────
        # URL BREAKDOWN
        # ─────────────
        st.markdown("---")
        st.subheader("🔎 URL Breakdown")

        domain = url.split('/')[2] if "://" in url else url

        st.write(f"**Domain:** {domain}")
        st.write(f"**URL Length:** {len(url)}")
        st.write(f"**Subdomains:** {domain.count('.')}")
        st.write(f"**Contains digits:** {'Yes' if any(c.isdigit() for c in url) else 'No'}")
        st.write(f"**Contains @ symbol:** {'Yes' if '@' in url else 'No'}")

        # ─────────────
        # EXPLANATION
        # ─────────────
        st.markdown("---")
        st.subheader("🧠 Why this result?")

        reasons = []

        if len(url) > 75:
            reasons.append("URL is unusually long")

        if domain.count('.') > 2:
            reasons.append("Too many subdomains")

        if any(c.isdigit() for c in domain):
            reasons.append("Domain contains suspicious digits")

        if '-' in domain:
            reasons.append("Domain uses hyphens (common in phishing)")

        if '@' in url:
            reasons.append("Contains '@' symbol (can hide real domain)")

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("No strong phishing indicators detected.")

        # ─────────────
        # REPORT BUTTON
        # ─────────────
        st.markdown("---")
        import urllib.parse

st.markdown("---")
st.subheader("🚨 Report Suspicious URL")

if url:
    encoded_url = urllib.parse.quote(url)

    st.markdown(
        f"""
        - 🔗 [Report to Google Safe Browsing](https://safebrowsing.google.com/safebrowsing/report_phish/?url={encoded_url})
        - 🔗 [Submit to PhishTank](https://phishtank.org/submit.php)
        """
    )
else:
    st.info("Enter a URL to enable reporting links.")