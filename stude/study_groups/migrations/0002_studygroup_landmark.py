# Generated by Django 4.2.3 on 2023-09-24 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landmarks', '0001_initial'),
        ('study_groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='landmark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='landmarks.landmark'),
        ),
    ]
