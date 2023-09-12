from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets
from .models import Subject, SubjectInstance
from .serializers import SubjectInstanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SubjectListAllView(generics.ListAPIView):
    serializer_class = SubjectInstanceSerializer
    queryset = SubjectInstance.objects.all()

    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SubjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubjectInstance.objects.all()
    serializer_class = SubjectInstanceSerializer

    def get(self, request):
        user = self.request.user
        user_course = user.course
        # If user is irregular, show all subjects in his/her course to choose from
        if (user.irregular):
            subjects = SubjectInstance.objects.filter(
                course__name=user_course)

        # Else, return subjects that match the user's student info (Year Level, Semster, Course)
        else:
            user_yearlevel = user.year_level
            user_semester = user.semester
            subjects = SubjectInstance.objects.filter(
                course__name=user.course, year_level__name=user_yearlevel, semester__name=user_semester)

        # Serialize the subjects
        serializer = SubjectInstanceSerializer(subjects, many=True)
        return Response(serializer.data)


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
    serializer_class = SubjectInstanceSerializer

    def get(self, request, course_slug, year_slug, semester_slug):
        # Retrieve the subjects based on year level and semester slugs
        subjects = SubjectInstance.objects.filter(
            course__shortname=course_slug, year_level__shortname=year_slug, semester__shortname=semester_slug)
        # Serialize the subjects
        serializer = SubjectInstanceSerializer(subjects, many=True)
        return Response(serializer.data)
