from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.gis.geos import Point
from study_groups.models import StudyGroup
from student_status.models import StudentStatus


class Command(BaseCommand):
    help = 'Removes old study groups and resets old student statuses'

    def handle(self, *args, **kwargs):
        # Get the current time
        now = timezone.now()

        # Get the time 8 hours ago
        time_threshold = now - timezone.timedelta(hours=8)

        # Delete StudyGroup entries older than 8 hours
        StudyGroup.objects.filter(timestamp__lt=time_threshold).delete()

        # Get StudentStatus entries older than 8 hours
        old_statuses = StudentStatus.objects.filter(
            timestamp__lt=time_threshold)

        # Set the fields of the old statuses to the required values
        for status in old_statuses:
            status.location = Point(0, 0)
            status.subject = None
            status.landmark = None
            status.study_group = None
            status.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully cleaned old entries'))
