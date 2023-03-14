from django.contrib import admin
from apps.oauth2.models import OauthClient, OauthClientUuid

admin.site.register(OauthClient)
admin.site.register(OauthClientUuid)
