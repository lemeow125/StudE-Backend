from rest_framework import generics
from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectByYearSemesterView(generics.ListAPIView):
    def get(self, request, year_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = Subject.objects.filter(
            year_level__shortname=year_slug)

        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)
