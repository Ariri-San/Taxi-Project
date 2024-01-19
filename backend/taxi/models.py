from django.db import models

# Create your models here.

class Price_Mile(models.Model):
    name = models.CharField(_(""), max_length=50)