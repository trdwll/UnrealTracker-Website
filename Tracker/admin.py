from django.contrib import admin
from .models import Item, Category

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author', 'slug']

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)