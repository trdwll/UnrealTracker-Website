from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{str(self.title)}'
    
class Item(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.URLField()
    current_price = models.CharField(max_length=2048)
    previous_prices = models.CharField(max_length=2048)
    # rating 
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.title}'

    def has_changed_price_within_sale(self):
        return False
    
    def has_previous_prices(self):
        return self.previous_prices is not ''

