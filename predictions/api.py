from typing import Optional
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prediction
from .serializers import PredictionSerializer

class HistoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.first_name or 'patient'
        qs = Prediction.objects.all()
        patient_username: Optional[str] = request.query_params.get('patient')
        if role == 'doctor':
            if patient_username:
                try:
                    patient_user = User.objects.get(username=patient_username)
                except User.DoesNotExist:
                    return Response({"error": "Patient not found"}, status=404)
                qs = qs.filter(user=patient_user)
            else:
                qs = qs.filter(doctor=request.user)
        else:
            qs = qs.filter(user=request.user)
        serializer = PredictionSerializer(qs, many=True)
        return Response(serializer.data)