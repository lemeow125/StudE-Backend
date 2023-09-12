from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Semester
from .serializers import SemesterSerializer


class SemesterListView(generics.ListAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()

    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
