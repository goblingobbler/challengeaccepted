from django.contrib import admin
from models import *
# Register your models here.

class ChallengeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Challenge, ChallengeAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comments, CommentAdmin)