from django.contrib.auth.models import AbstractUser
from django.db import models


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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Email inherited from base user class
    # Username inherited from base user class
    # Password inherited from base user class
    # is_admin inherited from base user class
    is_student = models.BooleanField(default=True)
    is_studying = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    year_level = models.CharField(
        max_length=50, choices=YEAR_LEVELS)
    semester = models.CharField(
        max_length=50, choices=SEMESTERS)
    avatar = models.ImageField(upload_to='avatars', null=True)
    pass
