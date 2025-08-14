from django.db import models
from django.contrib.auth.models import User
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_cents = models.BigIntegerField(default=0)
    def balance(self):
        return self.balance_cents / 100.0
    def __str__(self):
        return f"{self.user.username} - {self.balance()}"