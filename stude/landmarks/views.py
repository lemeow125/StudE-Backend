from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import LandmarkSerializer


class LandmarkListView(generics.ListAPIView):
    serializer_class = LandmarkSerializer
    permission_classes = [IsAuthenticated]
