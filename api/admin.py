from django.contrib import admin
from .models import UserProfile, Document, Order
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Order)
