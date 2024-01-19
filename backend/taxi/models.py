from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.




class Price_Mile(models.Model):
    days = [""]
    name = models.CharField(_("Name"), max_length=50)
    days = models.Choices()
    MEMBERSHIP_ARTIST = 'A'
    MEMBERSHIP_CUSTOMER = 'C'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_ARTIST, 'Artist'),
        (MEMBERSHIP_CUSTOMER, 'Customer'),
    ]
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_CUSTOMER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)





class Price_Day(models.Model):
    satrt = models.DateField()