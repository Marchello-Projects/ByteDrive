from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    storage_limit = models.BigIntegerField(
        default=104857600, verbose_name="Limit (bytes)"
    )
    used_storage = models.BigIntegerField(default=0, verbose_name="Used (bytes)")

    def __str__(self):
        return f"{self.username} ({self.used_storage} / {self.storage_limit})"


class MediaFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files"
    )

    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(editable=False, default=0)
    file_type = models.CharField(max_length=50, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (ID: {self.id})"
