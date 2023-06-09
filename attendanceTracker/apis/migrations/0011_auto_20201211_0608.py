# Generated by Django 3.1.3 on 2020-12-11 06:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_auto_20201211_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytics',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='analytics',
            name='modified_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='modified_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(6, 8, 0, 188195)),
        ),
        migrations.AlterField(
            model_name='crash',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='crash',
            name='modified_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='office',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='office',
            name='modified_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
