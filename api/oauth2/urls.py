from django.urls import path

from api.oauth2.views.oauth import OauthClientRedirectAPIView

urlpatterns = [
    path('/authorize/', OauthClientRedirectAPIView.as_view())

]