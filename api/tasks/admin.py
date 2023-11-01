from django.contrib import admin

from .models import Tag, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["title", "owner"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["title", "owner"]

