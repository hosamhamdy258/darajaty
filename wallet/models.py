from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from .errors import InsufficientBalance

CURRENCY_STORE_FIELD = getattr(settings, "WALLET_CURRENCY_STORE_FIELD", models.BigIntegerField)


# TODO force validation (can't deposit negative number same for withdraw )
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    current_balance = CURRENCY_STORE_FIELD(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, value):
        if value <= 0:
            raise ValueError("Deposit amount must be positive")
        self.transaction_set.create(
            value=value,
            previous_balance=self.current_balance,
            running_balance=self.current_balance + value,
        )
        self.current_balance += value
        self.save()

    def withdraw(self, value):
        if value <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if value > self.current_balance:
            raise InsufficientBalance("This wallet has insufficient balance.")
        self.transaction_set.create(
            value=-value,
            previous_balance=self.current_balance,
            running_balance=self.current_balance - value,
        )
        self.current_balance -= value
        self.save()

    def transfer(self, wallet, value):
        self.withdraw(value)
        wallet.deposit(value)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    value = CURRENCY_STORE_FIELD(default=0)
    running_balance = CURRENCY_STORE_FIELD(default=0)
    previous_balance = CURRENCY_STORE_FIELD(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
