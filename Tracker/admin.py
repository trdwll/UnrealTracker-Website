from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author', 'slug']

admin.site.register(Item, ItemAdmin)