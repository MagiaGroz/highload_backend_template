import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(db_index=True, unique=True)
    image = models.ImageField(upload_to='images/users/', default=None, null=True)
    phone = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=20
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
