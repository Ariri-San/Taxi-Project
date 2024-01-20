from django.db import models
# from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid
# Create your models here.


class PriceMile(models.Model):
    name = models.CharField(max_length=255)


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

    day_of_week = models.CharField(max_length=1, choices=DAY_CHOICES)
    priceday = models.ForeignKey(PriceDay, on_delete=models.CASCADE)
    pricemile = models.ForeignKey(PriceMile, on_delete=models.CASCADE)


class FixedPrice(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    destination = models.CharField(max_length=255)


class Travel(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    date_return = models.DateField(blank=True, null=True)
    present = models.DateField(auto_now_add=True)
    travel_code = models.UUIDField(unique=True,default=uuid.uuid4, editable=False, max_length=36)
    origin = models.CharField(max_length=511)
    destination = models.CharField(max_length=511)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    


class History(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    date_return = models.DateField()
    confirmed = models.DateField(auto_now_add=True)
    travel_code = models.UUIDField(unique=True,default=uuid.uuid4, editable=False, max_length=36)
    origin = models.CharField(max_length=511)
    destination = models.CharField(max_length=511)