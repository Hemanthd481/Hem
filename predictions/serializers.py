from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            'id', 'user', 'doctor', 'features', 'predicted_class', 'probabilities', 'labels', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'doctor', 'predicted_class', 'probabilities', 'labels', 'created_at']