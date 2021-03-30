from django.core.management.base import BaseCommand, CommandError

from Tracker.models import Item, Category

from pathlib import Path
import os, json, datetime



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = 'imports the data from the data.json file'

    def handle(self, *args, **options):
        with open(f'{BASE_DIR}\data.json', 'r') as data_file:
            jsondata = json.loads(data_file.read())

            # remove non-unique slugs
            d = {each['slug'] : each for each in jsondata}.values()
            #x = {"title": "SteamBridge", "author": "TRDWLL", "image": "https://cdn1.epicgames.com/ue/product/Thumbnail/SteamBridge_thumb-284x284-0af782db1f80e468d8322d97ba384077.png?resize=1&w=300", "current_price": "9.99", "slug": "steambridge"}
            
            for x in d:
                title = x['title']
                category = x['category']
                print(category)
                author = x['author']
                image = x['image']
                new_current_price = x['current_price']
                slug = x['slug']
                current_date = datetime.datetime.now()

                tmp_new_price = {"price": new_current_price, "date": str(current_date)}

                category_obj, category_created = Category.objects.get_or_create(title=category)
                obj, created = Item.objects.get_or_create(slug=slug, category=category_obj)
                if category_created:
                    category_obj.slug = x['categoryslug']
                    category_obj.save()

                if created:
                    obj.title = title 
                    obj.category = category_obj
                    obj.author = author 
                    obj.current_price = tmp_new_price 
                    obj.image = image
                    obj.save()
                else:
                    db_current_price = json.loads(obj.current_price.replace('\'','"'))
                    if new_current_price == db_current_price['price']:
                        pass
                    else:
                        # print(f'the fresh price isn\'t the same as the one in the DB so lets add the db_current_price to the previous prices and update the current_price - {str(title)}')

                        previous_prices = []
                        if obj.previous_prices:
                            previous_prices_data = obj.previous_prices.replace('\'','"')
                            previous_prices = json.loads(previous_prices_data)
                        previous_prices.append(db_current_price)

                        # TODO: sort previous prices by date
                        obj.previous_prices = previous_prices
                        obj.current_price = tmp_new_price

                        # TODO: The author is able to change the category so we should probably set it here also

                        print(f'({str(title)}) tmp_new_price: {str(tmp_new_price)}')

                        obj.save()
