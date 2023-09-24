from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer
from .models import StudyGroup
from subjects.models import Subject, SubjectInstance
from student_status.models import StudentStatus
from rest_framework import generics, viewsets, exceptions
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class StudyGroupListView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def partial_update(self, instance, request, *args, **kwargs):
        # Ensure only "users" field is being updated
        if set(request.data.keys()) != {"users"}:
            return Response({"detail": "Only the 'users' field can be updated."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current list of users
        instance = self.get_object()
        current_users = set(instance.users.values_list('id', flat=True))

        # Get the new list of users from the request
        new_users = set(request.data['users'])

        # Check if the only difference between the two sets is the current user
        diff = current_users.symmetric_difference(new_users)
        if len(diff) > 1 or (len(diff) == 1 and request.user.id not in diff):
            return Response({"detail": "You can only add or remove yourself from the study group."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the study group if there are no users left
        instance = self.get_object()
        if not instance.users.exists():
            instance.delete()

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the current user is the creator of the study group
        # Assuming 'date_joined' is a field in your User model
        creator = instance.users.all().first()
        if request.user != creator:
            return Response({"detail": "Only the creator can delete the study group."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the current user is the only one in the study group
        if instance.users.count() > 1:
            return Response({"detail": "The study group cannot be deleted if there are other users in it."}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

        # Get the user's course
        user_course = user.course
        print(user_course)

        # Get the subject name of the student's subjects from SubjectInstance
        user_subject_names = user.subjects.values_list('subject', flat=True)
        print('user subjects:', user_subject_names)
        # Get the corresponding Subject models
        user_subjects = Subject.objects.filter(name__in=user_subject_names)
        # Now fetch the StudyGroups with the matching Subject models
        studygroups = StudyGroup.objects.filter(subject__in=user_subjects)

        for group in studygroups:
            # Get all StudentStatus locations of the group
            group_locations = group.users.values_list('location', flat=True)
            # Convert string locations to GEOSGeometry objects
            point_locations = [fromstr(loc, srid=4326)
                               for loc in group_locations]
            # Calculate distances between every pair of locations
            distances = [(loc1.distance(
                loc2)*100000)for loc1 in point_locations for loc2 in point_locations]
            # Get the maximum distance
            group_radius = max(distances) if distances else 0
            group_radius = max(group_radius, 15)
            # Annotate the group with the radius
            group.radius = group_radius
        return studygroups


class StudyGroupListNearView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()
        user_location = fromstr(
            user_status.location, srid=4326)

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

        if user_status.active is False:
            raise exceptions.ValidationError("Student Status is not active")

        # Get the user's course
        user_course = user.course
        print(user_course)

        # Get the subject name of the student's subjects from SubjectInstance
        user_subject_names = user.subjects.values_list('subject', flat=True)
        # Get the corresponding Subject models
        user_subjects = Subject.objects.filter(name__in=user_subject_names)

        # Now fetch the StudyGroups with the matching Subject models that are within 100m
        studygroups = StudyGroup.objects.filter(subject__in=user_subjects).annotate(
            distance=Distance('location', user_location)).filter(distance__lte=100)

        for group in studygroups:
            # Get all StudentStatus locations of the group
            group_locations = group.users.values_list('location', flat=True)
            # Convert string locations to GEOSGeometry objects
            point_locations = [fromstr(loc, srid=4326)
                               for loc in group_locations]
            # Calculate distances between every pair of locations
            distances = [(loc1.distance(
                loc2)*100000)for loc1 in point_locations for loc2 in point_locations]
            # Get the maximum distance
            group_radius = max(distances) if distances else 0
            group_radius = max(group_radius, 15)
            # Annotate the group with the radius
            group.radius = group_radius

        return studygroups


class StudyGroupMembershipViewSet(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()
