# Generated by Django 4.2.2 on 2023-06-27 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('year_levels', '0001_initial'),
        ('accounts', '0004_alter_customuser_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='year_levels.year_level'),
        ),
    ]
