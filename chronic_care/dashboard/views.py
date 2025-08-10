from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Count
from accounts.models import User
from predictor.models import Prediction


def is_doctor(user):
    return user.is_authenticated and getattr(user, 'role', None) == User.Roles.DOCTOR


@login_required
@user_passes_test(is_doctor)
def analytics(request):
    by_disease = (
        Prediction.objects.values('disease')
        .annotate(total=Count('id'))
        .order_by('disease')
    )
    by_outcome = (
        Prediction.objects.values('disease', 'result')
        .annotate(total=Count('id'))
        .order_by('disease', 'result')
    )
    context = {
        'by_disease': list(by_disease),
        'by_outcome': list(by_outcome),
    }
    return render(request, 'doctor/analytics.html', context)