from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Accounts(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(max_length=100, unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        return self.email
