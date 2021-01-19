from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_profile_image_to(instance, filename):
    """
    custom path for saving images

    Returns:
        str: image path
    """
    asset_path = f'sample-chat/{str(instance.id)}/images/{filename}'
    return asset_path


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False)
    profile_image = models.ImageField(
        upload_to=upload_profile_image_to, blank=True, null=True)
