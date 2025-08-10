from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def role_redirect(user):
    if user.is_authenticated and hasattr(user, 'role'):
        if user.is_doctor():
            return redirect('patients:list')
        return redirect('patients:patient_home')
    return redirect('accounts:login')


@login_required
def home(request):
    return role_redirect(request.user)