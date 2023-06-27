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
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    subject = models.CharField(max_length=100, null=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
