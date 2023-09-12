from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Year_Level
from .serializers import YearLevelSerializer


class CourseListView(generics.ListAPIView):
    serializer_class = YearLevelSerializer
    queryset = Year_Level.objects.all()

    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
