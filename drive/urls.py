from django.urls import path
from .views import RegisterView, CustomLoginView, FileListCreateView, FileDetailView, AdminAllFilesView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('files/', FileListCreateView.as_view(), name='file-list'),
    path('admin/all-files/', AdminAllFilesView.as_view(), name='admin-all-files'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail')
]