from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('followings',)
    
admin.site.register(Profile, ProfileAdmin)


