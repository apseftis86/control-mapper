from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    pass


class Organization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    role = models.ForeignKey(Role, related_name='users', null=True, on_delete=models.SET_NULL)
    failed_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_name(self):
        return f'{self.first_name} {self.last_name}'
