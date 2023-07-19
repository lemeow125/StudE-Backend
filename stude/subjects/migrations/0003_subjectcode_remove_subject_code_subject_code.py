# Generated by Django 4.2.3 on 2023-07-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_alter_subject_code_alter_subject_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='code',
        ),
        migrations.AddField(
            model_name='subject',
            name='code',
            field=models.ManyToManyField(to='subjects.subjectcode'),
        ),
    ]