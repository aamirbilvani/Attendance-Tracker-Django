# Generated by Django 3.1.3 on 2020-12-11 06:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0011_auto_20201211_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceuser',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='attendanceuser',
            name='isactive',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='attendanceuser',
            name='modified_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(6, 11, 34, 453852)),
        ),
    ]
