# Generated by Django 2.0.5 on 2019-03-23 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdu', '0002_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unionid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]