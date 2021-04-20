from django.db import models
from django.urls import reverse
import json, datetime
from dateutil.parser import parse

from .utils import process_time

PREVIOUS_SALES = [
   # {"date_start": "2021-01-15 10:00:00", "date_end": "2021-01-20 23:59:59"}
]

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
    ratings = models.CharField(max_length=1024, default='', blank=True)
    slug = models.SlugField(unique=True, max_length=250)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('product-view', kwargs={'slug': self.slug })

    def has_changed_price_within_sale(self):
        if self.previous_prices:
            for psdate in PREVIOUS_SALES:
                try:
                    previous_prices = json.loads(self.previous_prices.replace('\'', '"'))
                    start_date = psdate['date_start']
                    end_date = psdate['date_end']

                    # check if the previous prices have changed within 7 days of a sale
                    for date in previous_prices:
                        previous_date = date['date']
                        result = process_time(parse(str(previous_date)), parse(start_date), parse(end_date))
                        if result:
                            return True
                except json.decoder.JSONDecodeError:
                    break

        return False

    def has_previous_prices(self):
        return self.previous_prices != ''

