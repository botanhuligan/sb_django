# Generated by Django 2.2.6 on 2019-10-24 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191024_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='load_test',
        ),
    ]
