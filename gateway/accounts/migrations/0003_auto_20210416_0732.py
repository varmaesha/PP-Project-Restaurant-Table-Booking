# Generated by Django 3.1.7 on 2021-04-16 07:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210416_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previousorders',
            name='ordertime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
