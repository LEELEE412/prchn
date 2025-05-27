import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import DepositProducts, SavingProducts



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
    # 팔로우 기능 (비대칭 self‐referential M2M)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )
    @property
    def active_subscriptions(self):
        now = timezone.now()
        return self.subscriptions.filter(end_date__gt=now)
    

class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    product = models.ForeignKey(
        DepositProducts,
        on_delete=models.CASCADE
    )
    term_months = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.term_months * 30)
        super().save(*args, **kwargs)

    def get_remaining_days(self):
        now = timezone.now()
        return max(0, (self.end_date - now).days)

    def __str__(self):
        return f"{self.user.username} ▶ 예금 ▶ {self.product.fin_prdt_cd}"


class UserSavingSubscription(models.Model):
    """
    Model to track user's saving product subscriptions.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saving_subscriptions'
    )
    product = models.ForeignKey(
        SavingProducts,
        on_delete=models.CASCADE
    )
    term_months = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.term_months * 30)
        super().save(*args, **kwargs)

    def get_remaining_days(self):
        now = timezone.now()
        return max(0, (self.end_date - now).days)

    def __str__(self):
        return f"{self.user.username} ▶ 적금 ▶ {self.product.fin_prdt_cd}"
