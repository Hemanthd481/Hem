from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    patient_code = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"Patient({self.user.username})"
