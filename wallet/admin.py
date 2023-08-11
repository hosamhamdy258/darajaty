from django.contrib import admin

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "current_balance", "created_at")
    list_filter = ("user", "created_at")
    date_hierarchy = "created_at"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "wallet",
        "previous_balance",
        "value",
        "running_balance",
        "created_at",
    )
    list_filter = ("wallet", "created_at")
    date_hierarchy = "created_at"
