import time
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
import os
from courses.models import Course


def validate_student_id(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError('Student ID must be a valid integer.')


class CustomUser(AbstractUser):
    YEAR_LEVELS = (
        ('1st', '1st year'),
        ('2nd', '2nd year'),
        ('3rd', '3rd year'),
        ('4th', '4th year'),
        ('5th', '5th Year'),
        ('Irreg', 'Irregular'),
    )
    SEMESTERS = (
        ('1st', '1st semester'),
        ('2nd', '2nd semester'),
    )

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
    year_level = models.CharField(
        max_length=50, choices=YEAR_LEVELS)
    semester = models.CharField(
        max_length=50, choices=SEMESTERS)
    avatar = models.ImageField(upload_to=_get_upload_to, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    pass
