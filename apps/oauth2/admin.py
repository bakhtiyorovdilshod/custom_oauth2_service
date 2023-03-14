from django.contrib import admin
from apps.oauth2.models import OauthClient, OauthClientUuid, OAuth2Token, AuthorizationCode

admin.site.register(OauthClient)
admin.site.register(OauthClientUuid)
admin.site.register(OAuth2Token)
admin.site.register(AuthorizationCode)
