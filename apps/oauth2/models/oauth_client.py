from authlib.oauth2.rfc6749 import ClientMixin
from django.contrib.auth.models import User

from .base import BaseModel
from django.db import models


class OauthClient(BaseModel, ClientMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=48, unique=True, db_index=True)
    client_secret = models.CharField(max_length=48, blank=True)
    name = models.CharField(max_length=120)
    redirect_url = models.TextField(default='')
    scope = models.TextField(default='')
    response_type = models.TextField(default='')
    grant_type = models.TextField(default='')

    def __str__(self):
        return self.name


class OauthClientUuid(BaseModel):
    client = models.ForeignKey(OauthClient, on_delete=models.CASCADE)
    uuid = models.UUIDField()

    def __str__(self):
        return f'{self.client.name}'
