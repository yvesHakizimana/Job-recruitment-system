# Generated by Django 5.1.2 on 2024-10-24 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmployeeProfile',
            new_name='EmployerProfile',
        ),
    ]
