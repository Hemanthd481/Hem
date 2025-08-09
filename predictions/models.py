from django.contrib.auth.models import User
from django.db import models


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_predictions')
    features = models.JSONField()
    predicted_class = models.IntegerField()
    probabilities = models.JSONField()
    labels = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Prediction(user={self.user.username}, cls={self.predicted_class}, at={self.created_at:%Y-%m-%d %H:%M})"
