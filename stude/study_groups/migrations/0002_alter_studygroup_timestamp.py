# Generated by Django 4.2.5 on 2023-10-13 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
