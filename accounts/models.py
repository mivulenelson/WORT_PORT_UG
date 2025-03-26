import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username,password=None,  **extra_fields):

        if not email and username:
            raise ValueError("User must have an email address and a username")

        if not "@gmail.com" in email:
            raise ValueError("You must sign in with a valid Gmail account.")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Super user must have 'is_admin'=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have 'is_staff'=True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have 'is_active'=True")

        user = self.create_user(
            email,
            username,
            **extra_fields,
            password=password
        )
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionManager):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True, verbose_name="ID")
    email = models.EmailField(unique=True, max_length=225, verbose_name="Email address")
    username = models.CharField(max_length=30, verbose_name="Username")
    contact = models.CharField(max_length=15, verbose_name="User contact")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.is_admin