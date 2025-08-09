from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_view, name='prediction_form'),
    path('api/predict/', views.predict_api, name='predict_api'),
]