from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('announcements/', include('announcements.urls')),
    path('patients/', include('patients.urls')),
    path('chat/', include('chat.urls')),
    path('predict/', include('predictor.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(pattern_name='accounts:home', permanent=False)),
]