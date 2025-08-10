from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),
    path('create/', views.create_patient, name='create'),
    path('assign-room/', views.assign_room, name='assign_room'),
    path('patient/home/', views.patient_home, name='patient_home'),
]