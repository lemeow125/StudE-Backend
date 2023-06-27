# Generated by Django 4.2.2 on 2023-06-27 15:21

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
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
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
