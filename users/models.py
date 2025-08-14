import uuid
import random
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to='profile-images/',
        default="images/default_user.png"
    )
    bio = models.CharField(max_length=350, default="", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_verify_code(self):
        code = f"{random.randint(0, 9999):04}"
        EmailConfirmation.objects.create(
            user=self,
            code=code
        )
        return code

    @property
    def is_verified(self):
        return self.verified


class EmailConfirmation(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify')
    expiration_time = models.DateTimeField(null=True, db_index=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'code')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
