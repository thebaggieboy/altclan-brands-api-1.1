
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets
from .serializers import UserSerializer, ProfileSerializer, BrandUserSerializer, BlogSerializer
from brands.serializers import BrandDashboardSerializer
from .models import Profile, CustomUser, BrandUser
from brands.models import BrandDashboard, Blog
from django.conf import settings
#BrandUser = settings.BRAND_USER_MODEL

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class BrandUserViewSet(viewsets.ModelViewSet):
    queryset = BrandUser.objects.all()
    serializer_class = BrandUserSerializer

class BrandDashboardViewSet(viewsets.ModelViewSet):
    queryset = BrandDashboard.objects.all()
    serializer_class = BrandDashboardSerializer
    
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    
    


"""class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client
"""

