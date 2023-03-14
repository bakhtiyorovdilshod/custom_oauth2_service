from rest_framework.response import Response
from rest_framework.views import APIView

from api.oauth2.serializers.oauth import OauthClientRedirectSerializer


class OauthClientRedirectAPIView(APIView):
    def get(self, request):
        serializer = OauthClientRedirectSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        response = Response()
        response['Location'] = f"https://id.mf.uz/?client_id={data['client_id']}&token_id={data['token_id']}"
        return response