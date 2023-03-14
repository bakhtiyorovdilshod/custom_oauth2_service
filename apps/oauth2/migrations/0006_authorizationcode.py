# Generated by Django 3.2.2 on 2023-03-14 20:49

import apps.oauth2.models.oauth_token
import authlib.oauth2.rfc6749.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apps_oauth2', '0005_auto_20230314_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('client_id', models.CharField(db_index=True, max_length=48)),
                ('code', models.CharField(max_length=120, unique=True)),
                ('issued_at', models.IntegerField(default=apps.oauth2.models.oauth_token.now_timestamp)),
                ('expires_in', models.IntegerField(default=0)),
                ('is_alive', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, authlib.oauth2.rfc6749.models.AuthorizationCodeMixin),
        ),
    ]
