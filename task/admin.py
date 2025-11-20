from django.contrib import admin

from .models import Category, Tag, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "due_date", "completed")
    list_filter = ("completed", "category", "tags")
    search_fields = ("title", "description")
    autocomplete_fields = ("category", "tags")
