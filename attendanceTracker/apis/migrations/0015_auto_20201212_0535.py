# Generated by Django 3.1.3 on 2020-12-12 05:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0014_auto_20201211_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 12, 12), null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(5, 35, 31, 517195)),
        ),
    ]
