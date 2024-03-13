from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.PriceMile)
admin.site.register(models.PriceDay)
admin.site.register(models.FixedPrice)
admin.site.register(models.JoinedPrice)
admin.site.register(models.Travel)
admin.site.register(models.History)
admin.site.register(models.Location)
