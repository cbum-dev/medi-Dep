# Generated by Django 4.2.7 on 2024-08-18 17:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Socials', '0003_chatroom_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='content',
        ),
        migrations.AddField(
            model_name='blog',
            name='body',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]