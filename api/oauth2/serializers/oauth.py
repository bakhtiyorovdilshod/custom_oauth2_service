from django.contrib.auth.models import User
from rest_framework import serializers
import uuid
from django.db import transaction

from apps.oauth2.models import OauthClient, OauthClientUuid, AuthorizationCode, OAuth2Token


class OauthClientRedirectSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=300)
    response_type = serializers.CharField(max_length=30, write_only=True)
    redirect_url = serializers.CharField(max_length=300, write_only=True)
    code_challenge = serializers.CharField(max_length=300, write_only=True)
    code_challenge_method = serializers.CharField(max_length=30, write_only=True)
    token_id = serializers.CharField(max_length=100, read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=OauthClient.objects.all(), required=False)

    def validate(self, attrs):
        client = OauthClient.objects.filter(
            client_id=attrs['client_id']
        ).first()
        if not client:
            raise serializers.ValidationError({'message': 'client has not found'})
        attrs['client'] = client
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        token_id = uuid.uuid4()
        client_uuid = OauthClientUuid.objects.create(
            client=validated_data['client'],
            uuid=uuid.uuid4()
        )
        return {'client_id': validated_data['client_id'], 'token_id': token_id}


class OauthClientTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=300, write_only=True)
    client_secret = serializers.CharField(max_length=300, write_only=True)
    redirect_url = serializers.CharField(max_length=300, write_only=True)
    grant_type = serializers.CharField(max_length=100, write_only=True)
    code = serializers.UUIDField(write_only=True)
    access_token = serializers.CharField(max_length=100, read_only=True)
    refresh_token = serializers.CharField(max_length=100, read_only=True)
    token_type = serializers.CharField(max_length=100, read_only=True)
    expires_in = serializers.CharField(min_length=30, read_only=True)

    def validate(self, attrs):
        code = AuthorizationCode.objects.filter(
            client_id=attrs['client_id'],
            code=attrs['code']

        ).first()
        if not code:
            raise serializers.ValidationError({'message': 'code has not found'})
        client = OauthClient.objects.filter(
            client_id=attrs['client_id'],
            client_secret=attrs['client_secret']
        ).first()
        if not client:
            raise serializers.ValidationError({'message': 'client has not found'})
        return attrs

    def create(self, validated_data):
        token = OAuth2Token.objects.filter(
            client_id=validated_data['client_id'],
            user=User.objects.all().first()
        ).first()
        return {
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600
        }



