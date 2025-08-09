from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from .models import Patient


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('home')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'doctor' or 'patient'
        if not username or not password or role not in {'doctor', 'patient'}:
            return render(request, 'accounts/register.html', {'error': 'Fill all fields correctly.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.first_name = role
        user.save()
        return redirect('login')
    return render(request, 'accounts/register.html')


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    role = request.user.first_name or 'patient'
    return render(request, 'accounts/dashboard.html', {'role': role})


@login_required
def create_patient_view(request: HttpRequest) -> HttpResponse:
    role = request.user.first_name or 'patient'
    if role != 'doctor':
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'accounts/create_patient.html', {'error': 'Username and password required'})
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/create_patient.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.first_name = 'patient'
        user.save()
        code = get_random_string(8).upper()
        while Patient.objects.filter(patient_code=code).exists():
            code = get_random_string(8).upper()
        Patient.objects.create(user=user, doctor=request.user, patient_code=code)
        return render(request, 'accounts/create_patient.html', {'success': f'Patient created with code: {code}'})
    return render(request, 'accounts/create_patient.html')
