from django.urls import path

from api.oauth2.views.oauth import OauthClientRedirectAPIView, OauthClientCodeGenerateAPIView, OauthClientTokenAPIView

urlpatterns = [
    path('authorize/', OauthClientRedirectAPIView.as_view()),
    path('generate/', OauthClientCodeGenerateAPIView.as_view()),
    path('token/', OauthClientTokenAPIView.as_view())

]