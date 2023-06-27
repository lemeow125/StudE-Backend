from rest_framework import generics
from .models import Year_Level
from .serializers import YearLevelSerializer


class CourseListView(generics.ListAPIView):
    serializer_class = YearLevelSerializer
    queryset = Year_Level.objects.all()
