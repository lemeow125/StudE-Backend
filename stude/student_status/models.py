from django.db import models
from accounts.models import CustomUser
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class StudentStatus(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    location = gis_models.PointField(blank=True, null=True, srid=4326)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.SET_NULL, null=True, to_field='name')
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    landmark = models.ForeignKey(
        'landmarks.Landmark', on_delete=models.SET_NULL, null=True)
    study_group = models.ForeignKey(
        'study_groups.StudyGroup', on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return self.user.full_name


@receiver(post_save, sender=CustomUser)
def create_student_status(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentStatus.objects.create(user=instance)
