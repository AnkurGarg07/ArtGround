from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.shippingInfo)
admin.site.register(models.couponInfo)
admin.site.register(models.productReview)