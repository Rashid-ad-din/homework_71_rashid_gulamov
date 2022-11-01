from django.contrib.auth.models import UserManager as BaseManager
from django.db.models import QuerySet, Avg


class UserManager(BaseManager):
    def create_superuser(self, username=None, login=None, email=None, password=None, **extra_fields):
        username = login if not username else username
        # extra_fields['login'] = login
        return super(UserManager, self).create_superuser(username, email, password, **extra_fields)
