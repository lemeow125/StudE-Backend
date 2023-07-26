# Generated by Django 4.2.3 on 2023-07-26 03:53

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_status', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('active', models.BooleanField(default=False)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject')),
            ],
        ),
        migrations.CreateModel(
            name='StudyGroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_groups.studygroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_status.studentstatus')),
            ],
        ),
        migrations.AddField(
            model_name='studygroup',
            name='users',
            field=models.ManyToManyField(through='study_groups.StudyGroupMembership', to='student_status.studentstatus'),
        ),
    ]
