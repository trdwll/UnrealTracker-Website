from django.db import models

class Price(models.Model):
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'${str(self.amount)}'
    
class Item(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    # category
    image = models.URLField()
    current_price = models.CharField(max_length=2048)
    previous_prices = models.CharField(max_length=2048)
    # rating 
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.title}'

