# Generated by Django 5.0 on 2023-12-18 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_datetime', models.DateTimeField()),
                ('is_rescheduled', models.BooleanField(default=False)),
                ('problem', models.TextField(default='Something wrong with my health')),
                ('healthcare_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.healthcareprovider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='HealthcareRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(default='pdfs/default.pdf', upload_to='pdfs/')),
                ('healthcare_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.healthcareprovider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.user')),
            ],
        ),
    ]
