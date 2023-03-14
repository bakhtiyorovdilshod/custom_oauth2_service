from rest_framework import serializers
import uuid
from django.db import transaction

from apps.oauth2.models import OauthClient, OauthClientUuid


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
