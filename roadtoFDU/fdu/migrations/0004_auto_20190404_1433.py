# Generated by Django 2.1.7 on 2019-04-04 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fdu', '0003_user_unionid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='unionid',
            new_name='sessionid',
        ),
    ]
