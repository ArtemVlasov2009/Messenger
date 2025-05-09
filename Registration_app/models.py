from django.db import models

# Create your models here.

class Send_Reg_Code(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
