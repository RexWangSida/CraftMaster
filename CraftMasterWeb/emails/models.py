from django.db import models
from datetime import date
# Create your models here.
class Email(models.Model):
    email = models.CharField(max_length=60,unique=True)
    register_date = models.DateField(default=date.today)

    def __str__(self):
        return self.email
