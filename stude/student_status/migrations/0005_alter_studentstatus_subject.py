# Generated by Django 4.2.2 on 2023-07-04 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_subjectstudent_subject_students'),
        ('student_status', '0004_alter_studentstatus_study_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentstatus',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subjects.subject'),
        ),
    ]
