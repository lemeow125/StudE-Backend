from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


def validate_student_id(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError('Student ID must be a valid integer.')


class CustomUser(AbstractUser):
    # Function for avatar uploads
    def _get_upload_to(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        # Get the student ID number
        ext = base_filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)

        student_id = str(instance.student_id_number)
        new_filename = f"{student_id}_{filename}_{file_extension}"
        return os.path.join('avatars', new_filename)

    # Delete old avatar file if new one is uploaded
    def save(self, *args, **kwargs):
        try:
            # is the object in the database yet?
            this = CustomUser.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(CustomUser, self).save(*args, **kwargs)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Email inherited from base user class
    # Username inherited from base user class
    # Password inherited from base user class
    # is_admin inherited from base user class
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_studying = models.BooleanField(default=False)
    irregular = models.BooleanField(default=False)
    student_id_number = models.CharField(
        max_length=16, validators=[validate_student_id], null=False)
    avatar = models.ImageField(upload_to=_get_upload_to, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True
    )
    year_level = models.ForeignKey(
        Year_Level,
        on_delete=models.SET_NULL,
        null=True
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True
    )
    subjects = models.ManyToManyField('subjects.Subject')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    pass


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'accounts':
        User = CustomUser
        username = os.getenv('DJANGO_ADMIN_USERNAME')
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')

        if not User.objects.filter(username=username).exists():
            # Create the superuser with is_active set to False
            superuser = User.objects.create_superuser(
                username=username, email=email, password=password)

            # Activate the superuser
            superuser.is_active = True
            superuser.save()

        User = CustomUser
        username = 'keannu125'
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')
        student_id_number = '2020300490'
        first_name = 'Keannu'
        last_name = 'Bernasol'
        # course = 'Bachelor of Science in Information Technology'
        # year_level = '1st Year'
        # semester = '1st Semester'

        if not User.objects.filter(username=username).exists():
            # Create the superuser with is_active set to False
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name, student_id_number=student_id_number)

            # Activate the superuser
            user.is_active = True
            user.save()
