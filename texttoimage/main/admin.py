from django.contrib import admin
from main.models import TextToImage


@admin.register(TextToImage)
class TextToImageAdmin(admin.ModelAdmin):
    list_display = ("prompt", "image", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
