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


def validate_student_id(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError('Student ID must be a valid integer.')


class CustomUser(AbstractUser):
    def _get_upload_to(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        # Convert filename to a slug format
        cleaned_filename = slugify(base_filename)
        # Get the student ID number
        student_id = str(instance.student_id_number)
        new_filename = f"{student_id}_{cleaned_filename}{file_extension}"
        return os.path.join('avatars', new_filename)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Email inherited from base user class
    # Username inherited from base user class
    # Password inherited from base user class
    # is_admin inherited from base user class
    is_student = models.BooleanField(default=True)
    is_studying = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    student_id_number = models.CharField(
        max_length=16, validators=[validate_student_id], null=False)
    avatar = models.ImageField(upload_to=_get_upload_to, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True
    )
    year_level = models.ForeignKey(
        Year_Level,
        on_delete=models.CASCADE,
        null=True
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        null=True
    )
    subjects = models.ManyToManyField(
        'subjects.Subject', through='subjects.SubjectStudent', related_name='SubjectStudent_user')

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
            User.objects.create_superuser(
                username, email, password)
