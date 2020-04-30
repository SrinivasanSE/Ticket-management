from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    technician = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
