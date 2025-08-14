from django.db import models
from django.contrib.auth.models import User
class WithdrawalRequest(models.Model):
    STATUS = [('PENDING','PENDING'),('APPROVED','APPROVED'),('REJECTED','REJECTED')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_cents = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(blank=True, null=True)
    def amount(self):
        return self.amount_cents / 100.0
    def __str__(self):
        return f"{self.user.username} - {self.amount()} - {self.status}"