from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')
        return self.create_user(email, password, **extra_fields)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('member', 'Member'),
        ('merchant', 'Merchant'),
        ('executive', 'Executive'),
        ('seller', 'Seller'),
        ('superuser', 'Superuser'),
    ]

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    
    # Hierarchy Links
    assigned_merchant = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='merchant_members', limit_choices_to={'role': 'merchant'}
    )
    assigned_executive = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='executive_merchants', limit_choices_to={'role': 'executive'}
    )
    assigned_seller = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='seller_executives', limit_choices_to={'role': 'seller'}
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Manager Assignment
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} [{self.role}]"