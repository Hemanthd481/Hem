from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.list_announcements, name='list'),
    path('create/', views.create_announcement, name='create'),
]