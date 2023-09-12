from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import LandmarkSerializer
from .models import Landmark


class LandmarkListView(generics.ListAPIView):
    serializer_class = LandmarkSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Landmark.objects.all()

    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
