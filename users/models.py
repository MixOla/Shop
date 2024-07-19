from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal


class UserManager(BaseUserManager):
    def _create_user(self, email, password, profile_picture,
                     coupon_balance, **extra_fields):
        if not email:
            raise ValueError('You must write your email')
        if not password:
            raise ValueError('Password must be provided')

        user = self.model(
            email=self.normalize_email(email),
            profile_picture=profile_picture,
            coupon_balance=coupon_balance,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, 
                    profile_picture=None, coupon_balance=Decimal('0.00'),
                    **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, profile_picture, 
                                 coupon_balance, **extra_fields)

    def create_superuser(self, email=None, password=None, 
                         profile_picture=None, 
                         coupon_balance=Decimal('0.00'), **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, profile_picture,
                                 coupon_balance, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, unique=True)
    profile_picture = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    coupon_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    categories_bought = models.JSONField(default=dict)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
