# Generated by Django 4.2.6 on 2023-12-03 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
