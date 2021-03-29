from django.core.management.base import BaseCommand, CommandError

from Tracker.models import Item, Price

from pathlib import Path
import os, json, datetime



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = 'imports the data from the data.json file'

    def handle(self, *args, **options):
        with open(f'{BASE_DIR}\data.json', 'r') as data_file:
            jsondata = json.loads(data_file.read())
            for x in jsondata:
                title = x['title']
                author = x['author']
                image = x['image']
                new_current_price = x['current_price']
                slug = x['slug']
                current_date = '' #TODO

                tmp_new_price = {'price': new_current_price, 'date': str(datetime.datetime.now())}

                # if the new_current_price is different than the current_price in the db then add the new_current_price to the previous_prices and update the current_price with new_current_price
                obj = Item.objects.get_or_create(title=title, author=author, current_price=tmp_new_price, image=image, slug=slug)

