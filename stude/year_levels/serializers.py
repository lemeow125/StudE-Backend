from rest_framework import serializers
from .models import Year_Level


class YearLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year_Level
        fields = '__all__'
