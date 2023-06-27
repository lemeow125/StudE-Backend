from django.db import models
# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=64)
    course_shortname = models.CharField(max_length=16)

    def __str__(self):
        return self.course_shortname
