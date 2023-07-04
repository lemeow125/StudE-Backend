# Generated by Django 4.2.2 on 2023-06-27 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('semesters', '0001_initial'),
        ('year_levels', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=16)),
                ('courses', models.ManyToManyField(related_name='SubjectCourse_subject', through='courses.SubjectCourse', to='courses.course')),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='semesters.semester')),
                ('year_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Year_Level_name', to='year_levels.year_level')),
            ],
        ),
    ]