# Generated by Django 4.2.3 on 2023-09-30 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('first_name', 'last_name')},
        ),
    ]
