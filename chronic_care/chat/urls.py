from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('doctor/inbox/', views.doctor_inbox, name='doctor_inbox'),
    path('patient/', views.patient_chat, name='patient_chat'),
]