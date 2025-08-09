from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.form_view, name='prediction_form'),
    path('api/predict/', views.predict_api, name='predict_api'),
    path('api/history/', api.HistoryList.as_view(), name='predictions_history'),
]