from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.predict_home, name='home'),
    path('run/', views.run_prediction, name='run'),
]