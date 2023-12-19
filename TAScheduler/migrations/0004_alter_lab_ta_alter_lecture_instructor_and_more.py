# Generated by Django 4.2.7 on 2023-12-14 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TAScheduler', '0003_ta_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='ta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAScheduler.ta'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAScheduler.instructor'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='ta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAScheduler.ta'),
        ),
    ]