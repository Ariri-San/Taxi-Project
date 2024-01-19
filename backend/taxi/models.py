from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

class PriceMile(models.Model):
    name = models.CharField(_("Name"), max_length=50)


class PriceDay(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    satrt = models.DateField()
    finish = models.DateField()

class JoinedPrice(models.Model):
    SUNDAY = 'S'
    OTHERDAYS = 'O'

    DAY_CHOICES = [
    (SUNDAY, "Sunday"),
    (OTHERDAYS, "Otherdays"),
    ]

    day_of_week = models.Choices(max_length=1, choices=DAY_CHOICES)
    priceday = models.ForeignKey(PriceDay, on_delete=models.CASCADE)
    pricemile = models.ForeignKey(PriceMile, on_delete=models.CASCADE)

class FixedPrice(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    destination = models.CharField(max_length=255)