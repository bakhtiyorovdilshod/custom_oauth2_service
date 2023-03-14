import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
import re

from api.oauth2.utils.token import generate_token
from apps.oauth2.models import OAuth2Token, OauthClient, OauthClientUuid, AuthorizationCode


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, write_only=True)
    username = serializers.CharField(max_length=50, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    client = serializers.PrimaryKeyRelatedField(queryset=OauthClient.objects.all(), required=False)
    access_token = serializers.CharField(max_length=100, read_only=True)
    refresh_token = serializers.CharField(max_length=100, read_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'message': 'user has not found'})
        referer = self.context['request'].headers.get('Referer')
        if not referer:
            raise serializers.ValidationError({'message': 'please set up Referer in headers'})
        attrs['user'] = user
        uuid_extract_pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"
        uuids = re.findall(uuid_extract_pattern, referer)
        if len(uuids) != 1:
            raise serializers.ValidationError({'message': 'more than uuid sent'})
        client_uuid = OauthClientUuid.objects.filter(
            uuid=uuids[0]
        ).first()
        if not client_uuid:
            raise serializers.ValidationError({'message': 'uuid has been slept'})
        attrs['client'] = client_uuid.client
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        client_id = validated_data['client'].client_id
        oauth_token = OAuth2Token.objects.filter(
            user=user,
            is_alive=True
        ).first()
        if oauth_token:
            if not oauth_token.get_is_alive():
                access_token = oauth_token.access_token
                refresh_token = oauth_token.refresh_token
            else:
                access_token = generate_token(42)
                refresh_token = generate_token(48)
                OAuth2Token.objects.create(
                    client_id=client_id,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    user=validated_data['user'],
                    expires_in=3600
                )
        else:
            access_token = generate_token(42)
            refresh_token = generate_token(48)
            OAuth2Token.objects.create(
                client_id=client_id,
                access_token=access_token,
                refresh_token=refresh_token,
                user=validated_data['user'],
                expires_in=3600
            )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600
        }


class OauthClientCodeGenerateSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=300, write_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=OauthClient.objects.all(), required=False)
    code = serializers.UUIDField(read_only=True)
    redirect_url = serializers.CharField(max_length=100, read_only=True)

    def validate(self, attrs):
        client_uuid = OauthClientUuid.objects.filter(
            uuid=attrs.get('uuid'),
            is_alive=True
        ).first()
        if not client_uuid:
            raise serializers.ValidationError({'message': 'uuid has been expired'})
        attrs['client'] = client_uuid.client
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        client = validated_data['client']
        code = uuid.uuid4()
        AuthorizationCode.objects.create(
            client_id=client.client_id,
            user=User.objects.all().first(),
            code=code
        )
        return {'code': code, 'redirect_url': client.redirect_url}



