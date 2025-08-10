from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.forms import PatientCreationForm
from accounts.models import User
from .forms import RoomAssignmentForm
from .models import RoomAssignment
from announcements.models import Announcement


def is_doctor(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.DOCTOR


def is_patient(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.PATIENT


@login_required
@user_passes_test(is_doctor)
def patient_list(request):
    patients = User.objects.filter(role=User.Roles.PATIENT).select_related('patient_profile')
    return render(request, 'doctor/patients.html', {'patients': patients})


@login_required
@user_passes_test(is_doctor)
def create_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully')
            return redirect('patients:list')
    else:
        form = PatientCreationForm()
    return render(request, 'doctor/create_patient.html', {'form': form})


@login_required
@user_passes_test(is_doctor)
def assign_room(request):
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            room, created = RoomAssignment.objects.update_or_create(
                patient=form.cleaned_data['patient'],
                defaults={
                    'room_number': form.cleaned_data['room_number'],
                    'notes': form.cleaned_data.get('notes'),
                }
            )
            messages.success(request, f'Room assigned: {room.room_number}')
            return redirect('patients:list')
    else:
        form = RoomAssignmentForm()
    return render(request, 'doctor/assign_room.html', {'form': form})


@login_required
@user_passes_test(is_patient)
def patient_home(request):
    announcements = Announcement.objects.order_by('-created_at')[:10]
    room = getattr(request.user, 'room_assignment', None)
    return render(request, 'patient/home.html', {'announcements': announcements, 'room': room})