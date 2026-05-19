from django.db import models
from django.contrib.auth.models import User


TRANSACTION_TYPES = [
    ('purchase', 'Purchase'),
    ('transfer', 'Transfer'),
    ('withdrawal', 'Withdrawal'),
    ('deposit', 'Deposit'),
    ('payment', 'Payment'),
]

DEVICE_TYPES = [
    ('mobile', 'Mobile'),
    ('desktop', 'Desktop'),
    ('tablet', 'Tablet'),
    ('atm', 'ATM'),
    ('pos', 'POS Terminal'),
]


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    merchant = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    device = models.CharField(max_length=20, choices=DEVICE_TYPES)
    transaction_time = models.IntegerField(help_text="Hour of transaction (0-23)")
    status = models.CharField(max_length=10, choices=[('fraud', 'Fraud'), ('safe', 'Safe')])
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"TXN #{self.id} - {self.user.username} - {self.status.upper()} - ${self.amount}"

    @property
    def confidence_percent(self):
        return round(self.confidence * 100, 1)
