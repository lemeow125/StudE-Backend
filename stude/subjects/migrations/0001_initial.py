# Generated by Django 4.2.3 on 2023-07-26 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('semesters', '0001_initial'),
        ('year_levels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=16, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='semesters.semester')),
                ('students', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('year_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='year_levels.year_level')),
            ],
        ),
    ]
