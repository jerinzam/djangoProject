from django.contrib import admin
from .models import UserProfile, Document, Order, Shop, Organization
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Order)
admin.site.register(Shop)
admin.site.register(Organization)
