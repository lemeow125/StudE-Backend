from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import LandmarkSerializer
from .models import Landmark


class LandmarkListView(generics.ListAPIView):
    serializer_class = LandmarkSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Landmark.objects.all()
