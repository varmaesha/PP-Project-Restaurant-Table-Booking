# Generated by Django 3.1.7 on 2021-04-16 07:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210416_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previousorders',
            name='ordertime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
