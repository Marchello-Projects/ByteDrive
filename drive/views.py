from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from .docs import register_schema, login_schema

from .models import User
from .serializers import RegisterSerializer

@register_schema
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@login_schema
class CustomLoginView(ObtainAuthToken):
    pass