from django.db import models
from django.utils import timezone
from datetime import timedelta

class Send_Reg_Code(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=10))
