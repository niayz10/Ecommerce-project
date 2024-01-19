from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from . import choices

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            is_active=True
        )

        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=email, phone_number=phone_number)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True          )
    username = None
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone_number = PhoneNumberField(unique=True)
    user_type = models.CharField(
        choices=choices.UserType.choices, 
        null=True,
        blank=True,
        max_length=8,
        )
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email',]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
