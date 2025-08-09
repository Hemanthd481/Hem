from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "doctor", "predicted_class", "created_at")
    search_fields = ("user__username", "doctor__username")
    list_filter = ("predicted_class", "created_at")
