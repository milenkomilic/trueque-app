# Generated by Django 4.2.7 on 2023-12-13 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trueque_web_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginattempt',
            name='successful',
            field=models.BooleanField(default=False),
        ),
    ]
