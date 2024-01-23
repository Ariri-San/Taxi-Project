from django.db import models
# from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid
# Create your models here.


class PriceMile(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name


class PriceDay(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.TimeField()
    finish = models.TimeField()
    
    def __str__(self) -> str:
        return f"{self.price}$ :  {self.start} - {self.finish}"


class JoinedPrice(models.Model):
    SUNDAY = 'S'
    OTHERDAYS = 'O'

    DAY_CHOICES = [
        (SUNDAY, "Sunday"),
        (OTHERDAYS, "Otherdays"),
    ]

    day_of_week = models.CharField(max_length=1, choices=DAY_CHOICES)
    priceday = models.ForeignKey(PriceDay, on_delete=models.CASCADE, related_name="joined_prices")
    pricemile = models.ForeignKey(PriceMile, on_delete=models.CASCADE, related_name="joined_prices")
    
    def __str__(self) -> str:
        return f"{self.pricemile.name}-{self.day_of_week} = {self.priceday.price}$ :  {self.priceday.start} - {self.priceday.finish}"


class FixedPrice(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    name = models.CharField(max_length=255)
    formated_address = models.CharField(max_length=511)
    

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
    price_per_mile = models.DecimalField(max_digits=4, decimal_places=2)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    passengers = models.PositiveSmallIntegerField(default=1)
    luggage = models.PositiveSmallIntegerField(default=1)
    date = models.DateField()
    date_return = models.DateField(blank=True, null=True)
    present = models.DateTimeField(auto_now_add=True)
    travel_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, max_length=36)
    origin = models.CharField(max_length=511)
    destination = models.CharField(max_length=511)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    
    def __str__(self) -> str:
        return f"{self.user} : {self.distance} mile = {self.price}$"


class History(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_mile = models.DecimalField(max_digits=4, decimal_places=2)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    passengers = models.PositiveSmallIntegerField(default=1)
    luggage = models.PositiveSmallIntegerField(default=1)
    date = models.DateField()
    date_return = models.DateField()
    confirmed = models.DateTimeField(auto_now_add=True)
    travel_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, max_length=36)
    origin = models.CharField(max_length=511)
    destination = models.CharField(max_length=511)
    
    def __str__(self) -> str:
        return f"{self.user} : {self.distance} mile = {self.price}$"
    