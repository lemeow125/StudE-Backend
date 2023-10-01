# Generated by Django 4.2.5 on 2023-10-01 16:37

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]
