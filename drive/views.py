from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema_view

from .models import User, MediaFile
from .serializers import RegisterSerializer, MediaFileSerializer, MediaFileUpdateSerializer
from .docs import (
    register_schema, 
    login_schema, 
    profile_schema, 
    file_list_schema,
    file_create_schema,
    admin_all_files_schema,
    file_update_schema,
    file_delete_schema
)

class UserFileMixin:
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return MediaFile.objects.select_related('owner').filter(owner=self.request.user).order_by('-created_at')

@register_schema
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@login_schema
class CustomLoginView(ObtainAuthToken):
    pass

@profile_schema
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    get=file_list_schema,
    post=file_create_schema
)
class FileListCreateView(UserFileMixin, generics.ListCreateAPIView):
    serializer_class = MediaFileSerializer

    def perform_create(self, serializer):
        file_obj = self.request.data.get('file') 
        serializer.save(
            owner=self.request.user,
            size=file_obj.size
        )

@extend_schema_view(
    patch=file_update_schema,
    delete=file_delete_schema
)
class FileDetailView(UserFileMixin, generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return MediaFileUpdateSerializer
        return MediaFileSerializer

    def perform_destroy(self, instance):
        instance.delete()

@admin_all_files_schema
class AdminAllFilesView(generics.ListAPIView):
    queryset = MediaFile.objects.select_related('owner').all().order_by('-created_at')
    serializer_class = MediaFileSerializer
    permission_classes = [IsAdminUser]