from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import MediaFile


@receiver(post_save, sender=MediaFile)
def update_storage_on_create(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        user.used_storage += instance.size
        user.save()


@receiver(post_delete, sender=MediaFile)
def update_storage_on_delete(sender, instance, **kwargs):
    user = instance.owner

    if user.used_storage >= instance.size:
        user.used_storage -= instance.size
        user.save()
