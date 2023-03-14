from rest_framework.response import Response
from rest_framework.views import APIView

from api.oauth2.serializers.client import OauthClientCodeGenerateSerializer
from api.oauth2.serializers.oauth import OauthClientRedirectSerializer, OauthClientTokenSerializer
from api.oauth2.utils.token import token_required
from rest_framework.permissions import IsAuthenticated


class OauthClientRedirectAPIView(APIView):
    def get(self, request):
        serializer = OauthClientRedirectSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        response = Response()
        response['Location'] = f"https://id.mf.uz/?client_id={data['client_id']}&token_id={data['token_id']}"
        return response


class OauthClientCodeGenerateAPIView(APIView):
    def post(self, request):
        serializer = OauthClientCodeGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OauthClientTokenAPIView(APIView):
    def get(self, request):
        serializer = OauthClientTokenSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)