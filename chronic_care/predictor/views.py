from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import numpy as np
from .models import Prediction
from .utils import load_model, prepare_input, REQUIRED_FEATURES


@login_required
def predict_home(request):
    context = {
        'diseases': Prediction.DISEASE_CHOICES,
        'required_features': REQUIRED_FEATURES,
    }
    return render(request, 'patient/predict.html', context)


@login_required
@require_http_methods(["POST"])
def run_prediction(request):
    disease = request.POST.get('disease')
    if disease not in dict(Prediction.DISEASE_CHOICES):
        messages.error(request, 'Invalid disease selected')
        return render(request, 'patient/predict.html', {'diseases': Prediction.DISEASE_CHOICES, 'required_features': REQUIRED_FEATURES})
    try:
        model = load_model(disease)
    except FileNotFoundError as e:
        messages.error(request, f'{e}. Please ask your doctor to train the models.')
        return render(request, 'patient/predict.html', {'diseases': Prediction.DISEASE_CHOICES, 'required_features': REQUIRED_FEATURES})

    data = {k: request.POST.get(k) for k in REQUIRED_FEATURES[disease]}
    X = prepare_input(disease, data)
    prob = 0.0
    if hasattr(model, 'predict_proba'):
        prob = float(model.predict_proba(X)[0][1])
    y_pred = int(model.predict(X)[0])
    record = Prediction.objects.create(
        user=request.user,
        disease=disease,
        input_data=data,
        result=bool(y_pred),
        probability=prob,
    )
    context = {
        'prediction': record,
        'diseases': Prediction.DISEASE_CHOICES,
        'required_features': REQUIRED_FEATURES,
    }
    return render(request, 'patient/predict.html', context)