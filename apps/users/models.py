from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CreatedUpdatedBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class User(AbstractUser):
    pass
    avatar = models.ImageField(null=True, verbose_name='avatar', upload_to='images/')
    birthday = models.DateTimeField(null=True)
    position = models.ForeignKey('positions.Position', on_delete=models.CASCADE, blank=True, null=True)
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'
        ordering = ['-id']

    def __str__(self):
        return self.username


class MyUserManager(BaseUserManager):

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
