# Generated by Django 2.2 on 2019-05-09 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_auto_20190503_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 9, 17, 44, 37, 149468)),
        ),
    ]
