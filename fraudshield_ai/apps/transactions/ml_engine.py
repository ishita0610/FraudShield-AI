"""
ML Engine for FraudShield AI
Handles model loading and fraud prediction
"""
import numpy as np
import pandas as pd
import joblib
import os
from django.conf import settings

_fraud_model = None
_scaler = None
_anomaly_model = None
_features = None 


def load_models():
    global _fraud_model, _scaler, _anomaly_model, _features
    models_dir = settings.ML_MODELS_DIR
    _fraud_model = joblib.load(os.path.join(models_dir, 'fraud_model.pkl'))
    _scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    _anomaly_model = joblib.load(os.path.join(models_dir, 'anomaly.pkl'))
    _features = joblib.load(os.path.join(models_dir, 'features.pkl'))


def get_models():
    global _fraud_model, _scaler, _anomaly_model, _features
    if _fraud_model is None:
        load_models()
    return _fraud_model, _scaler, _anomaly_model, _features


TRANSACTION_TYPE_MAP = {
    'purchase': 0, 'transfer': 1, 'withdrawal': 2, 'deposit': 3, 'payment': 4
}

DEVICE_MAP = {
    'mobile': 0, 'desktop': 1, 'tablet': 2, 'atm': 3, 'pos': 4
}


def predict_fraud(amount, transaction_type, merchant, location, device, transaction_time):
    """
    Predict whether a transaction is fraudulent.
    Returns: (is_fraud: bool, confidence: float, anomaly_score: float)
    """
    fraud_model, scaler, anomaly_model, features = get_models()

    type_encoded = TRANSACTION_TYPE_MAP.get(transaction_type, 0)
    merchant_encoded = hash(merchant) % 20
    location_encoded = hash(location) % 50
    device_encoded = DEVICE_MAP.get(device, 0)

    input_data = {
        "Amount": float(amount),
        "transaction_type": type_encoded,
        "merchant": merchant_encoded,
        "location": location_encoded,
        "device": device_encoded,
        "Time": float(transaction_time),
    }

    df_input = pd.DataFrame([input_data])

    df_input = df_input.reindex(columns=features, fill_value=0)

    df_input = df_input.replace(r'[^0-9\.-]', '', regex=True)

    df_input = df_input.apply(pd.to_numeric, errors='coerce')

    df_input = df_input.fillna(0)


    features_scaled = scaler.transform(df_input)

    fraud_proba = fraud_model.predict_proba(features_scaled)[0]
    is_fraud_rf = fraud_model.predict(features_scaled)[0] == 1

    anomaly_score = anomaly_model.decision_function(features_scaled)[0]
    is_anomaly = anomaly_model.predict(features_scaled)[0] == -1

    fraud_confidence = float(fraud_proba[1])

    
    if is_fraud_rf and is_anomaly:
        final_confidence = min(0.99, fraud_confidence * 1.2)
        is_fraud = True
    elif is_fraud_rf:
        final_confidence = fraud_confidence
        is_fraud = fraud_confidence > 0.5
    elif is_anomaly:
        final_confidence = max(0.55, fraud_confidence + 0.15)
        is_fraud = final_confidence > 0.5
    else:
        final_confidence = fraud_confidence
        is_fraud = False

    return is_fraud, final_confidence, anomaly_score
