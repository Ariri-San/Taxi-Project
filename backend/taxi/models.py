from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Price_Mile(models.Model):
    name = models.CharField(_("Name"), max_length=50)