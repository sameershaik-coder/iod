from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.home.lib import backend
from apps.home.models import Networth

# Create your models here.

class AssetType(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    networth = models.ForeignKey(Networth, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

