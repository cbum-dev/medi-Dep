# Generated by Django 5.0 on 2023-12-19 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_user_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialty',
            name='desc',
            field=models.TextField(default=' '),
        ),
    ]
