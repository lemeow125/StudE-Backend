from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer


class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
