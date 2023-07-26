from rest_framework import generics, viewsets
from .models import Subject, SubjectInstance
from .serializers import SubjectSerializer, SubjectInstanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectByCourseView(generics.ListAPIView):
    queryset = SubjectInstance.objects.all()
    serializer_class = SubjectInstanceSerializer

    def get(self, request, course_slug):
        # Retrieve the subjects based on course slug
        subjects = SubjectInstance.objects.filter(
            course__shortname=course_slug)

        # Serialize the subjects
        serializer = SubjectInstanceSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectByCourseYearSemesterView(generics.ListAPIView):
    queryset = SubjectInstance.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, course_slug, year_slug, semester_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = SubjectInstance.objects.filter(
            course__shortname=course_slug, year_level__shortname=year_slug, semester__shortname=semester_slug)
        # Serialize the subjects
        serializer = SubjectInstanceSerializer(subjects, many=True)
        return Response(serializer.data)
