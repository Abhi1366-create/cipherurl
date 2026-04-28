# CipherURL 
import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from xgboost import XGBClassifier

# Paths

DATA_PATH = "data/dataset.csv"
MODEL_PATH = "models/model.pkl"

# Load data 

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

#
df.columns = df.columns.str.strip().str.lower()

label_col = "type"

if label_col not in df.columns:
    raise Exception(f"❌ '{label_col}' not found")

print(f"Using label column: {label_col}")
print(df[label_col].value_counts())



df[label_col] = df[label_col].astype(str).str.lower()

df[label_col] = df[label_col].map({
    'phishing': 1,
    'legitimate': 0,
    '1': 1,
    '0': 0
})

df = df.dropna(subset=[label_col])

X = df.drop(columns=[label_col])
y = df[label_col]

print("Feature shape:", X.shape)

scale_pos_weight = (y == 0).sum() / (y == 1).sum()

# Trian test and val

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.2, stratify=y_trainval, random_state=42
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")


model = XGBClassifier(
    n_estimators=1500,
    max_depth=8,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    gamma=0.1,
    reg_lambda=1,
    reg_alpha=0.5,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric='logloss',
    early_stopping_rounds=50
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False
)

print("Model training complete")

# Threshold tunning

probs = model.predict_proba(X_test)[:, 1]

best_thresh = 0.5
best_f1 = 0

for t in np.arange(0.3, 0.7, 0.02):
    preds = (probs >= t).astype(int)
    f1 = f1_score(y_test, preds)
    if f1 > best_f1:
        best_f1 = f1
        best_thresh = t

print(f"Best threshold: {best_thresh:.2f}")

y_pred = (probs >= best_thresh).astype(int)

# Evaluation

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature impotance

importances = pd.Series(model.feature_importances_, index=X.columns)
print("\n Top 10 Features:")
print(importances.sort_values(ascending=False).head(10))

# Save model

os.makedirs("models", exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump((model, X.columns.tolist(), best_thresh), f)

print(f"\n Model saved → {MODEL_PATH}")