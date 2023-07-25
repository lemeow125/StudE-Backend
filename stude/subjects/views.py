from rest_framework import generics, viewsets
from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectByCourseView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, course_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = Subject.objects.filter(
            courses__shortname=course_slug).order_by('-subjectyearlevel')

        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)


class SubjectByCourseYearSemesterView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, course_slug, year_slug, semester_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = Subject.objects.filter(
            courses__shortname=course_slug, year_levels__shortname=year_slug, semesters__shortname=semester_slug)

        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)
