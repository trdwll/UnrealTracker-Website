import re, json, time, random, datetime
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.request import urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
from pathlib import Path
from itertools import chain

BASE_DIR = Path(__file__).resolve().parent.parent
MAX_THREADS = 30
content = []

def download_url(url):
    resp = urlopen(url).read()
    print(url)
    soup = BeautifulSoup(resp, 'html.parser')
    all_content = soup.find_all('div', {'class': 'asset-container catalog asset-full'})
    all_images = soup.find_all('img')
    all_prices = soup.find_all('span', {'class': 'asset-price'})
    all_titles = soup.find_all('a', {'class': 'mock-ellipsis-item mock-ellipsis-item-helper ellipsis-text'})
    all_authors = soup.find_all('div', {'class': 'creator ellipsis'})

    prices = []
    for price in all_prices:
        cur_price = re.search('((\$[0-9]+(\.[0-9]{2})?))', str(price))
        if cur_price == None:
            prices.append('Free')
        else:
            prices.append(str(cur_price.group()))

    images = [x['src'] for x in all_images]
    titles = [x.getText().replace('\'', '&#39;') for x in all_titles]
    authors = [x.getText().replace(chr(160),'') for x in all_authors]
    slugs = [x['href'].split('/product/')[1] for x in all_titles]

    content.append([{'title': title, 'author': author, 'image': image, 'current_price': current_price, 'slug': slug} for title, author, image, current_price, slug in zip(titles, authors, images, prices, slugs)])

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

text = urlopen('https://www.unrealengine.com/marketplace/en-US/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start=0').read()
soup = BeautifulSoup(text, 'html.parser')
amount_content = soup.find('li', attrs={'class': 'rc-pagination-total-text'})
amount = re.search('([0-9]{5})', str(amount_content)).group(1)
amount_of_pages = int(amount) / 100 + 1

urls = []
for i in range(int(amount_of_pages)):
    start = i * 100
    urls.append('https://www.unrealengine.com/marketplace/en-US/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start={}'.format(start))

main(urls)
# main(['https://www.unrealengine.com/marketplace/en-US/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start=0', 'https://www.unrealengine.com/marketplace/en-US/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start=100'])






# this below is used to test the data that comes in on 1 page to avoid doing a ton of requests when testing

# text = urlopen('https://www.unrealengine.com/marketplace/en-US/assets?count=100&sortBy=effectiveDate&sortDir=DESC&start=0').read()
# soup = BeautifulSoup(text, 'html.parser')
# all_content = soup.find_all('div', {'class': 'asset-container catalog asset-full'})
# all_images = soup.find_all('img')
# all_prices = soup.find_all('span', {'class': 'asset-price'})
# all_titles = soup.find_all('a', {'class': 'mock-ellipsis-item mock-ellipsis-item-helper ellipsis-text'})
# all_authors = soup.find_all('div', {'class': 'creator ellipsis'})

# prices = []
# for price in all_prices:
#     cur_price = re.search('((\$[0-9]+(\.[0-9]{2})?))', str(price))
#     if cur_price == None:
#         prices.append('Free')
#     else:
#         prices.append(str(cur_price.group()))

# images = [x['src'] for x in all_images]
# titles = [x.getText() for x in all_titles]
# slugs = [x['href'].replace('/marketplace/en-US/product/','') for x in all_titles]
# authors = [x.getText().replace(chr(160),'') for x in all_authors]

# page_content2 = {'data': [{'title': title, 'author': author, 'image': image, 'current_price': current_price, 'slug': slug} for title, author, image, current_price, slug in zip(titles, authors, images, prices, slugs)]}
# print(json.dumps(page_content2))

# with open('yeeto.json', "w") as fh:
#     print(page_content2)
#     fh.write(json.dumps(page_content2))