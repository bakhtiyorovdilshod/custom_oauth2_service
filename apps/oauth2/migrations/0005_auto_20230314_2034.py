# Generated by Django 3.2.2 on 2023-03-14 20:34

import apps.oauth2.models.oauth_token
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_oauth2', '0004_auto_20230314_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthclientuuid',
            name='expires_in',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oauthclientuuid',
            name='is_alive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='oauthclientuuid',
            name='issued_at',
            field=models.IntegerField(default=apps.oauth2.models.oauth_token.now_timestamp),
        ),
    ]