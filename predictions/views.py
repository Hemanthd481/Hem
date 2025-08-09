from pathlib import Path
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_breast_cancer
import numpy as np
from django.contrib.auth.models import User
from accounts.models import Patient
from .models import Prediction
import json

MODEL_PATH = Path(__file__).resolve().parent / 'rf_model.joblib'
META_PATH = MODEL_PATH.with_suffix('.json')
FEATURE_NAMES = None


def ensure_model() -> Dict[str, Any]:
    global FEATURE_NAMES
    if MODEL_PATH.exists():
        model = load(MODEL_PATH)
        if FEATURE_NAMES is None:
            if META_PATH.exists():
                import json
                FEATURE_NAMES = json.loads(META_PATH.read_text()).get('feature_names')
            if not FEATURE_NAMES:
                FEATURE_NAMES = list(load_breast_cancer().feature_names)
        return {"model": model, "feature_names": FEATURE_NAMES}
    data = load_breast_cancer()
    X = data.data
    y = data.target
    FEATURE_NAMES = list(data.feature_names)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    dump(model, MODEL_PATH)
    return {"model": model, "feature_names": FEATURE_NAMES, "accuracy": float(acc)}


def _get_labels() -> list:
    if META_PATH.exists():
        import json
        data = json.loads(META_PATH.read_text())
        labels = data.get('labels')
        if labels:
            return labels
    return ["benign", "malignant"]


@login_required
def form_view(request: HttpRequest) -> HttpResponse:
    ctx = ensure_model()
    return render(request, 'predictions/form.html', {"feature_names": ctx["feature_names"]})


@login_required
def predict_api(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=400)
    ctx = ensure_model()
    feature_names = ctx["feature_names"]
    try:
        payload = {name: float(request.POST.get(name, '0')) for name in feature_names}
    except ValueError:
        return JsonResponse({"error": "Invalid inputs"}, status=400)
    X = np.array([[payload[name] for name in feature_names]], dtype=float)
    y_pred = ctx["model"].predict(X)[0]
    proba = ctx["model"].predict_proba(X)[0].tolist()
    labels = _get_labels()
    # Save history
    doctor_user: User | None = None
    role = request.user.first_name or 'patient'
    if role == 'doctor':
        doctor_user = request.user
    else:
        try:
            doctor_user = request.user.patient_profile.doctor
        except Patient.DoesNotExist:
            doctor_user = None
    Prediction.objects.create(
        user=request.user,
        doctor=doctor_user,
        features=payload,
        predicted_class=int(y_pred),
        probabilities=proba,
        labels=labels,
    )
    return JsonResponse({"prediction": int(y_pred), "probabilities": proba, "labels": labels})
