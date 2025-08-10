import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / 'disease_models'

REQUIRED_FEATURES = {
    'diabetes': ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age'],
    'heart': ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'],
    'kidney': ['age','bp','sg','al','su','bgr','bu','sc','sod','pot','hemo','pcv']
}


def get_model_path(disease_key: str) -> Path:
    return MODELS_DIR / f"{disease_key}_model.pkl"


def load_model(disease_key: str):
    model_path = get_model_path(disease_key)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found for {disease_key} at {model_path}")
    return joblib.load(model_path)


def prepare_input(disease_key: str, data: dict) -> np.ndarray:
    features = REQUIRED_FEATURES[disease_key]
    values = []
    for f in features:
        v = data.get(f)
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = 0.0
        values.append(v)
    return np.array([values])