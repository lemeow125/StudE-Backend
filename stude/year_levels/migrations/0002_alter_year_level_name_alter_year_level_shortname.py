# Generated by Django 4.2.3 on 2023-07-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('year_levels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year_level',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='year_level',
            name='shortname',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]