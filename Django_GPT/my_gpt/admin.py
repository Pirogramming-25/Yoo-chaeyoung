from django.contrib import admin
from .models import InferenceHistory


@admin.register(InferenceHistory)
class InferenceHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "input_short", "created_at")
    list_filter = ("task", "created_at")
    search_fields = ("user__username", "input_text", "output_text")
    readonly_fields = ("created_at",)

    def input_short(self, obj):
        return obj.input_text[:30] + ("..." if len(obj.input_text) > 30 else "")

    input_short.short_description = "Input Text"