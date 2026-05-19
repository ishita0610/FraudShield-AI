from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiry = self.created_at + datetime.timedelta(minutes=5)
        return timezone.now() > expiry

    def __str__(self):
        return f"OTP for {self.user.username}"
