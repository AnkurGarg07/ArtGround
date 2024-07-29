from django.contrib import admin
from . import models
import Account

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Seller)
admin.site.register(models.Customer)
