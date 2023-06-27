from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer
from .models import StudyGroup
from courses.models import SubjectCourse
# Create your views here.


class StudyGroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):
        user = self.request.user

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

        # Get the user's course
        user_course = user.course
        print(user_course)
        # Get subject ids related to the user's course through SubjectCourse
        subject_ids = SubjectCourse.objects.filter(
            course=user_course
        ).values_list('subject', flat=True)

        print(subject_ids)

        # Now fetch the StudyGroups with the subjects from the obtained subject_ids
        studygroups = StudyGroup.objects.filter(subject_id__in=subject_ids)
        return studygroups


class StudyGroupMembershipViewSet(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()
