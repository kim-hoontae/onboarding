# Generated by Django 3.2.8 on 2021-10-27 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]