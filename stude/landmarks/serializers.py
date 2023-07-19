from .models import Landmark
from rest_framework import serializers


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = '__all__'
