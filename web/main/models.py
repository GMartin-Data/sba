from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Ajouter le champ is_approved
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username