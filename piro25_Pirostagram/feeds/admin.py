from django.contrib import admin
from .models import Feed, Comment, Story

# Register your models here.
class FeedAdmin(admin.ModelAdmin):
    exclude = ('like_users',)

admin.site.register(Feed, FeedAdmin)
admin.site.register(Comment)
admin.site.register(Story)