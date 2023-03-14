import os
import string
import random

from apps.oauth2.models import OAuth2Token

UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for _ in range(length))


def token_required(func):
    def inner(request, *args, **kwargs):
        print(request.META)
        # token = OAuth2Token.objects.filter(
        #     access_token=request.headers.get('Authorization')
        # )
        return func(request, *args, **kwargs)
    return inner

