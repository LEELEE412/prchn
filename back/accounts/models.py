import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product


def generate_membership_number():
    """
    Generate a unique 20-character membership number using UUID4.
    """
    return uuid.uuid4().hex[:20]


class User(AbstractUser):
    """
    Custom User model with profile fields, subscribed products, and follow relations.
    """
    profile_image = models.ImageField(
        upload_to='profiles/', blank=True, null=True
    )
    bio = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    current_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    salary = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    membership_number = models.CharField(
        max_length=20,
        unique=True,
        default=generate_membership_number,
        editable=False,
    )
    subscribed = models.ManyToManyField(
        Product,
        blank=True,
        related_name='subscribers',
        verbose_name='가입한 상품'
    )

    # 팔로우 기능 (비대칭 self‐referential M2M)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )
