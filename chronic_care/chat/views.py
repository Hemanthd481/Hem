from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from accounts.models import User
from .models import Message


def is_doctor(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.DOCTOR


def is_patient(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.PATIENT


@login_required
@user_passes_test(is_doctor)
def doctor_inbox(request):
    query = Q(receiver=request.user)
    conversations = Message.objects.filter(query).select_related('sender', 'receiver')
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        reply = request.POST.get('reply')
        if patient_id and reply:
            patient = User.objects.filter(id=patient_id, role=User.Roles.PATIENT).first()
            if patient:
                Message.objects.create(sender=request.user, receiver=patient, body=reply)
                messages.success(request, 'Reply sent')
                return redirect('chat:doctor_inbox')
    patients = User.objects.filter(role=User.Roles.PATIENT).order_by('username')
    return render(request, 'chat/doctor_inbox.html', {'messages_list': conversations, 'patients': patients})


@login_required
@user_passes_test(is_patient)
def patient_chat(request):
    doctor = User.objects.filter(role=User.Roles.DOCTOR).first()
    thread = []
    if doctor:
        thread = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=doctor)) |
            (Q(sender=doctor) & Q(receiver=request.user))
        ).order_by('created_at')
    if request.method == 'POST':
        body = request.POST.get('body')
        if doctor and body:
            Message.objects.create(sender=request.user, receiver=doctor, body=body)
            return redirect('chat:patient_chat')
    return render(request, 'chat/patient_chat.html', {'doctor': doctor, 'thread': thread})