# Generated by Django 5.0 on 2023-12-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0003_healthcarereport_delete_healthcarerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
