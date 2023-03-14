import time

from authlib.oauth2.rfc6749 import TokenMixin
from django.contrib.auth.models import User

from apps.oauth2.models.base import BaseModel
from django.db import models


def now_timestamp():
    return int(time.time())


class OAuth2Token(BaseModel, TokenMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=48, db_index=True)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=255, unique=True, null=False)
    refresh_token = models.CharField(max_length=255, db_index=True)
    scope = models.TextField(default='')
    revoked = models.BooleanField(default=False)
    issued_at = models.IntegerField(null=False, default=now_timestamp)
    expires_in = models.IntegerField(null=False, default=0)

    def get_client_id(self):
        return self.client_id

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
        return self.issued_at + self.expires_in