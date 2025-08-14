from django.db import models
from django.contrib.auth.models import User
class Transaction(models.Model):
    TYPE_CHOICES = [('DEPOSIT','DEPOSIT'),('WITHDRAW','WITHDRAW'),('PAYMENT','PAYMENT'),('ADJUST','ADJUST')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount_cents = models.BigIntegerField()
    reference = models.CharField(max_length=200, blank=True, null=True)
    meta = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def amount(self):
        return self.amount_cents / 100.0
    def __str__(self):
        return f"{self.user.username} {self.type} {self.amount()}"