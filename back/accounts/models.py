from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product

class User(AbstractUser):
    # 사용자가 가입한 금융상품(M2M)
    subscribed = models.ManyToManyField(
        Product,
        blank=True,
        related_name='subscribers',
        verbose_name='가입한 상품'
    )
