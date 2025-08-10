from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientProfile


class PatientCreationForm(UserCreationForm):
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=False)
    contact_number = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.PATIENT
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                age=self.cleaned_data.get('age') or None,
                gender=self.cleaned_data.get('gender') or None,
                contact_number=self.cleaned_data.get('contact_number') or None,
                address=self.cleaned_data.get('address') or None,
            )
        return user