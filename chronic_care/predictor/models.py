from django.db import models
from django.conf import settings


class Prediction(models.Model):
    DISEASE_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('heart', 'Heart Disease'),
        ('kidney', 'Chronic Kidney Disease'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    input_data = models.JSONField()
    result = models.BooleanField()
    probability = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.disease}: {self.result}"