from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from posts.managers import PostManager


class Post(models.Model):
    description = models.CharField(verbose_name='Описание', null=False, blank=False, max_length=200)
    image = models.ImageField(verbose_name='Фото', null=False, blank=False, upload_to='posts')
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='posts', null=False, blank=False,
                               on_delete=models.CASCADE)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    deleted_at = models.DateTimeField(verbose_name='Дата удаления', null=True, default=None)

    objects = PostManager()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()


class Comments(models.Model):
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='comments', null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(verbose_name='Публикация', to='posts.Post', related_name='comments', null=False,
                             blank=False, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Описание', null=False, blank=False, max_length=200)
