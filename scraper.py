import re, json, time, random, datetime
import concurrent.futures
from urllib.request import urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
from pathlib import Path
from itertools import chain

BASE_DIR = Path(__file__).resolve().parent.parent
MAX_THREADS = 10
content = []

def parse_data(text):
    json_data = json.loads(text)

    for x in json_data["data"]["elements"]:
        if x["priceValue"] > 0:
            current_price = x["price"] if x["priceValue"] == x["discountPriceValue"] else x["discountPrice"] # tbh the logic here is flawed as hell lol. discount should only be set if there's a discount Epic wtf
            has_discount = x["priceValue"] != x["discountPriceValue"]
        else:
            current_price = "Free"
            has_discount = False

        rating_json_data = json.loads(urlopen(f'https://www.unrealengine.com/marketplace/api/review/{x["id"]}/ratings/').read())

        category_slug = x["categories"][0]["path"].split('assets/')[1]
        content.append([
        {
            "title": x["title"], "category": x["categories"][0]["name"], "categoryslug": category_slug, "author": x["seller"]["name"], 
            "image": x["thumbnail"], "current_price": current_price, "current_price_discounted": has_discount, "slug": x["urlSlug"],
            "rating_data": rating_json_data["data"]
        }])

def download_url(url):
    resp = urlopen(url).read()
    print(url)
    parse_data(resp)
    time.sleep(random.uniform(1.0, 3.0))
    
def download_items(store_urls):
    threads = min(MAX_THREADS, len(store_urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, store_urls)

def main(store_urls):
    t0 = time.time()
    download_items(store_urls)
    t1 = time.time()

    # format the list to be 1 long list rather than multiple lists nested in a list - [['1'], ['2'], ...] -> ['1','2', ...]
    new_content = list(chain.from_iterable(content))

    with open("data.json", "w") as fh:
        fh.write(json.dumps(new_content))
        
    t2 = time.time()
    print(f"{t1-t0} seconds to download {len(store_urls)} pages. {t2-t1} seconds to save the data.")

    with open("last_updated.txt", "w") as fh:
        fh.write(str(datetime.datetime.now()))

    # format the data to be able to be imported into mysql


# format and set up the urls for the main method

urls = []
def gather_urls():
    text = json.loads(urlopen('https://www.unrealengine.com/marketplace/api/assets').read())
    amount = text["data"]["paging"]["total"]
    amount_of_pages = int(amount) / 100 + 1

    for i in range(int(amount_of_pages)):
        start = i * 100
        urls.append('https://www.unrealengine.com/marketplace/api/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start={}'.format(start))


gather_urls()
main(urls)






# this below is used to test the data that comes in on 1 page to avoid doing a ton of requests when testing

# text = urlopen('https://www.unrealengine.com/marketplace/api/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start=0').read()
# parse_data(text)

# new_content = list(chain.from_iterable(content))
# with open('yeeto.json', "w") as fh:
#     fh.write(json.dumps(new_content))
