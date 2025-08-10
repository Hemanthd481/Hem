from django.db import models
from django.conf import settings


class RoomAssignment(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_assignment')
    room_number = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Room {self.room_number} -> {self.patient.username}"