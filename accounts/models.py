from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.shortcuts import get_object_or_404

from accounts.managers import UserManager


class GenderChoices(TextChoices):
    MALE = 'male', 'Мужчина'
    FEMALE = 'female', 'Женщина'


class Account(AbstractUser):
    login = models.CharField(verbose_name='Логин', unique=True, null=False, blank=False, max_length=150)
    email = models.EmailField(verbose_name='Электронная почта', unique=True, null=False, blank=False)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars',
        verbose_name='Аватар'
    )
    user_info = models.TextField(verbose_name='Информация о пользователе', null=True, blank=True, max_length=2000)
    phone = models.CharField(verbose_name='Номер телефона', null=True, blank=True, max_length=100)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.MALE, verbose_name='Пол', null=True,
                              blank=True, max_length=250)

    liked_posts = models.ManyToManyField(verbose_name='Понравившиеся публикации', to='posts.Post',
                                         related_name='user_likes')
    subscriptions = models.ManyToManyField(verbose_name='Подписки', to='accounts.Account', related_name='subscribers')
    commented_posts = models.ManyToManyField(verbose_name='Прокомментированные публикации', to='posts.Post',
                                             related_name='user_comments')

    USERNAME_FIELD = 'login'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
