from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", "doctor", "patient_code")
    search_fields = ("user__username", "doctor__username", "patient_code")
