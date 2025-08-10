from django import forms
from django.core.exceptions import ValidationError
from .models import RoomAssignment


class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoomAssignment
        fields = ['patient', 'room_number', 'notes']

    def clean(self):
        cleaned = super().clean()
        patient = cleaned.get('patient')
        if patient and not patient.is_patient():
            raise ValidationError('Selected user is not a patient')
        return cleaned