from rest_framework import generics, viewsets
from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SubjectListAllView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request):
        user = self.request.user
        user_course = user.course
        # If user is irregular, show all subjects in his/her course to choose from
        if (user.irregular):
            subjects = Subject.objects.filter(
                course__name=user_course)

        # Else, return subjects that match the user's student info (Year Level, Semster, Course)
        else:
            user_yearlevel = user.year_level
            user_semester = user.semester
            subjects = Subject.objects.filter(
                course__name=user.course, year_level__name=user_yearlevel, semester__name=user_semester)

        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectByCourseView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, course_slug):
        # Retrieve the subjects based on course slug
        subjects = Subject.objects.filter(
            course__shortname=course_slug)

        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectByCourseYearSemesterView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, course_slug, year_slug, semester_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = Subject.objects.filter(
            course__shortname=course_slug, year_level__shortname=year_slug, semester__shortname=semester_slug)
        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
