from rest_framework.response import Response
from rest_framework.views import APIView

from api.oauth2.serializers.client import UserLoginSerializer


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)