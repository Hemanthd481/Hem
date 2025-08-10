from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Announcement
from accounts.models import User


def is_doctor(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.DOCTOR


@login_required
def list_announcements(request):
    items = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/list.html', {'announcements': items})


@login_required
@user_passes_test(is_doctor)
def create_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Announcement.objects.create(title=title, content=content, created_by=request.user)
            messages.success(request, 'Announcement posted')
            return redirect('announcements:list')
        messages.error(request, 'Title and content are required')
    return render(request, 'doctor/create_announcement.html')