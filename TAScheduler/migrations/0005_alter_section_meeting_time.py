# Generated by Django 4.2.7 on 2023-12-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAScheduler', '0004_alter_lab_ta_alter_lecture_instructor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='meeting_time',
            field=models.TextField(),
        ),
    ]
