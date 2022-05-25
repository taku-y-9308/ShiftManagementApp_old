# Generated by Django 3.2.12 on 2022-05-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftManagementApp', '0016_shift_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='public',
        ),
        migrations.AddField(
            model_name='shift',
            name='publish',
            field=models.BooleanField(default=True, verbose_name='publish'),
        ),
    ]
