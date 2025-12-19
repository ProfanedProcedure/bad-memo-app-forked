from django.contrib import admin
from .models import Memo, Tag

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
