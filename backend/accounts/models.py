from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DATA_ENTRY = "DATA_ENTRY", "Data Entry"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DATA_ENTRY,
    )

    def __str__(self):
        return self.username