from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
import re

from api.oauth2.utils.token import generate_token
from apps.oauth2.models import OAuth2Token, OauthClient


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    client = serializers.PrimaryKeyRelatedField(queryset=OauthClient.objects.all(), required=False)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'message': 'user has not found'})
        referer = self.context['request'].META.get('Referer')
        if not referer:
            raise serializers.ValidationError({'message': 'please set up Referer in headers'})
        attrs['user'] = user
        uuid_extract_pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"
        uuids = re.findall(uuid_extract_pattern, referer)
        if len(uuids) == 1:
            raise serializers.ValidationError({'message': 'more than uuid sent'})
        client = OauthClient.objects.filter(
            uuid=uuids[0]
        ).first()
        if not client:
            raise serializers.ValidationError({'message': 'uuid has been slept'})
        attrs['client'] = client
        return attrs

    def create(self, validated_data):
        token = generate_token()
        OAuth2Token.objects.create(
            client_id=validated_data['client'].client_id,
            access_token=token,
            refresh_token=token,
            user=validated_data['user'],
            expires_in=3600

        )
        return {'access_token': token, 'refresh_token': token}

