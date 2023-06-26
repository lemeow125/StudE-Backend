from django.db import models
from accounts.models import CustomUser

# Create your models here.


class StudentStatus(models.Model):
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
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    x_latitude = models.FloatField(null=True)
    y_latitude = models.FloatField(null=True)
    subject = models.CharField(max_length=100)
    year_level = models.CharField(
        max_length=50, choices=CustomUser.YEAR_LEVELS)
    semester = models.CharField(max_length=50, choices=CustomUser.SEMESTERS)
    timestamp = models.DateField(auto_now_add=True)
