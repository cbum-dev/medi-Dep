# Generated by Django 5.0 on 2023-12-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_specialty_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcareprovider',
            name='fees',
            field=models.IntegerField(default=1200),
        ),
    ]
