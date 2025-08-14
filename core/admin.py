from django.contrib import admin
from .models import Wallet
from .transactions import Transaction
from .withdrawals import WithdrawalRequest
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','balance_cents')
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','type','amount_cents','reference','created_at')
@admin.register(WithdrawalRequest)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user','amount_cents','status','created_at')
    actions = ['approve_withdrawal','reject_withdrawal']
    def approve_withdrawal(self, request, queryset):
        from django.utils import timezone
        for wr in queryset.filter(status='PENDING'):
            wallet = wr.user.wallet
            if wallet.balance_cents >= wr.amount_cents:
                wallet.balance_cents -= wr.amount_cents
                wallet.save()
                wr.status = 'APPROVED'
                wr.processed_at = timezone.now()
                wr.save()
    approve_withdrawal.short_description = 'Approve selected withdrawals'
    def reject_withdrawal(self, request, queryset):
        for wr in queryset.filter(status='PENDING'):
            wr.status = 'REJECTED'
            wr.save()
    reject_withdrawal.short_description = 'Reject selected withdrawals'