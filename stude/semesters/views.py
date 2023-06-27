from rest_framework import generics
from .models import Semester
from .serializers import SemesterSerializer


class SemesterListView(generics.ListAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
