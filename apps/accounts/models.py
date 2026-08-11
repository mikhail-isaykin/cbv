from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from pytils.translit import slugify as pytils_slugify


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    slug = AutoSlugField(
        populate_from='user.username',
        unique=True,
        editable=True,
        slugify=pytils_slugify,
    )
    avatar = models.ImageField(
        upload_to='images/avatars/%Y/%m/%d',
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=(
                    'png',
                    'jpg',
                    'webp',
                    'jpeg',
                    'gif',
                ),
            ),
        ],
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})
