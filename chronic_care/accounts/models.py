from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        DOCTOR = 'DOCTOR', _('Doctor')
        PATIENT = 'PATIENT', _('Patient')

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PATIENT)

    def is_doctor(self) -> bool:
        return self.role == self.Roles.DOCTOR

    def is_patient(self) -> bool:
        return self.role == self.Roles.PATIENT


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"PatientProfile({self.user.username})"