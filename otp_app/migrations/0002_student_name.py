# Generated by Django 5.0.1 on 2024-11-14 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='Unknown', max_length=40),
        ),
    ]