from django.contrib import admin
from models import *
# Register your models here.

from factors.models import FactorAd

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    pass

admin.site.register(User, UserAdmin)
