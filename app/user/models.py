from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('username', email)
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def user_avatar_directory_path(instance, filename):
    # files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    dt_string = datetime.now().strftime("%d%m%Y%H%M%S_")
    filename = dt_string + filename
    return 'user_{0}/avatar/{1}'.format(instance.id, filename)


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, blank=True, null=True) # noqa: 501
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'
