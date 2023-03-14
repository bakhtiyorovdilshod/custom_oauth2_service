from rest_framework import serializers


class OauthClientRedirectSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=300)
    response_type = serializers.CharField(max_length=30)
    redirect_url = serializers.CharField(max_length=300)
    code_challenge = serializers.CharField(max_length=300)
    code_challenge_method = serializers.CharField(max_length=30)

    def validate(self, attrs):
        pass