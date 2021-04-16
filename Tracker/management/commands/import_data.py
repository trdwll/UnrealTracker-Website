from django.core.management.base import BaseCommand, CommandError

from Tracker.models import Item, Category

import os, json, time, random, datetime
import concurrent.futures
from urllib.request import urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
from pathlib import Path

# Pillow isn't supported by FreeBSD without ports and I cba to install ports
#from PIL import Image

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

def download_file(url, resource):
    file_name = Path(url).name
    name = f'{BASE_DIR}\\static\\thumbs\\{file_name}'
    with open(name, "wb") as fiel:
        fiel.write(resource.read())
        # img = Image.open(name)
        # img.save(name, optimize=True, quality=85)
        # img.close()

def download_url(url):
    resource = urlopen(url)
    download_file(url, resource)
    time.sleep(random.uniform(1.0, 3.0))

def download_items(image_urls):
    threads = min(10, len(image_urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, image_urls)

class Command(BaseCommand):
    help = 'imports the data from the data.json file'


    def handle(self, *args, **options):
        with open(f'{BASE_DIR}/data.json', 'r') as data_file:
            jsondata = json.loads(data_file.read())

            # remove non-unique slugs
            d = {each['slug'] : each for each in jsondata}.values()
            #d = [{"title": "SteamBridge", "category": "Code Plugins", "categoryslug": "codeplugins", "author": "TRDWLL", "image": "https://cdn1.epicgames.com/ue/product/Thumbnail/SteamBridge_thumb-284x284-0af782db1f80e468d8322d97ba384077.png", "current_price": "1.99", "current_price_discounted": False, "slug": "steambridge"}]
            
            i = 0
            for x in d:
                i += 1
                print(i)
                title = x['title']
                category = x['category']
                author = x['author']
                image = x['image']
                new_current_price = x['current_price']
                slug = x['slug']
                current_date = datetime.datetime.now()
                tmp_new_price = {"price": new_current_price, "date": str(current_date), "discounted": x["current_price_discounted"]}

                category_obj, category_created = Category.objects.get_or_create(title=category, slug=x['categoryslug'])
                item_obj = Item.objects.filter(slug=slug).first()
                if item_obj:
                    # item exists so we need to update it
                    print(f'======== The item ({title}) exists so we\'re going to update it')
                    item_obj.title = title
                    item_obj.author = author
                    item_obj.image = image
                    item_obj.category = category_obj
                    item_obj.save()
                else:
                    # item doesn't exist so lets create it
                    print(f'======== The item ({title}) doesn\'t exist so we\'re going to create it')
                    item_obj = Item(title=title, author=author, category=category_obj)
                    item_obj.slug = slug
                    item_obj.current_price = tmp_new_price 
                    item_obj.image = image
                    item_obj.save()
                    continue
                
                try:
                    db_current_price = json.loads(item_obj.current_price.replace('\'','"').replace('False', 'false'))
                    if new_current_price == db_current_price['price'] or x["current_price_discounted"]: 
                        continue
                    else:
                        try:
                            previous_prices = []
                            if item_obj.previous_prices:
                                previous_prices_data = item_obj.previous_prices.replace('\'','"').replace('False', 'false')
                                previous_prices = json.loads(previous_prices_data)
                            previous_prices.append(db_current_price)

                            # TODO: sort previous prices by date
                            item_obj.previous_prices = previous_prices

                        except json.decoder.JSONDecodeError as ex:
                            print('Loop error', ex)

                        item_obj.current_price = tmp_new_price

                        # TODO: The author is able to change the category so we should probably set it here also

                        print(f'({str(title)}) tmp_new_price: {str(tmp_new_price)}')

                        item_obj.save()
                except json.decoder.JSONDecodeError as ex:
                    print('End Loop', ex)

        # download last 100 images and update them in the db (caching)
        items = Item.objects.all().order_by('-id')[:3]
        urls = []
        for x in items:
            urls.append(x.image)
            name = Path(x.image).name
            x.image = f'https://unrealtracker.com/static/thumbs/{name}'
            x.save()

            
        download_items(urls)
