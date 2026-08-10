from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify as pytils_slugify


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        DRAFT = 'DF', 'Draft'

    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='author_posts',
    )
    updater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updater_posts',
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        blank=True,
        upload_to='images/posts/%Y/%m/%d/',
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
    slug = AutoSlugField(populate_from='title', unique=True, editable=True, slugify=pytils_slugify)
    fixed = models.BooleanField(default=False)
    excerpt = models.CharField(max_length=155, blank=True)
    description = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PostManager()

    class Meta:
        ordering = ('-fixed', '-created_at')
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        # indexes = [models.Index(fields=[

    def __str__(self):
        return f'{self.title} — {self.category} [{self.get_status_display()}]'

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = Truncator(self.description).chars(155, truncate='...')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        blank=True,
        upload_to='images/categories/%Y/%m/%d/',
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
    slug = AutoSlugField(populate_from='title', unique=True, editable=True, slugify=pytils_slugify)
    description = models.TextField(blank=True)

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        # indexes = [models.Index(fields=[

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_from_category', kwargs={'slug': self.slug})
