# Generated by Django 4.2.2 on 2023-06-26 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_studentstatus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentStatus',
        ),
    ]