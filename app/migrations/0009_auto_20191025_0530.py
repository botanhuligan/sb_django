# Generated by Django 2.2.6 on 2019-10-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20191025_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.TextField(default='Empty Tittle', max_length=255, verbose_name='Title'),
        ),
    ]
