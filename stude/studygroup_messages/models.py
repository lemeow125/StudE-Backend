from django.db import models
from study_groups.models import StudyGroup

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    message_content = models.TextField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: User={self.user.full_name}, Study_group={self.study_group.name}, ID={self.id}'
