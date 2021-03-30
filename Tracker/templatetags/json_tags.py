
import json
from django import template

from Tracker.utils import process_time
from Tracker.models import Item, PREVIOUS_SALES

register = template.Library()

@register.filter(name='parsejson')
def parsejson(str, arg):
    new_str = json.loads(str.replace('\'','"'))
    return new_str[arg]


# @register.filter(name='has_changed_price_within_sale')
# def has_changed_price_within_sale(date):
#     if self.previous_prices:
#         for psdate in PREVIOUS_SALES:
#             previous_prices = json.loads(self.previous_prices.replace('\'', '"'))
#             start_date = psdate['date_start']
#             end_date = psdate['date_end']

#             # check if the previous prices have changed within 7 days of a sale
#             for date in previous_prices:
#                 previous_date = date['date']
#                 result = process_time(parse(str(previous_date)), parse(start_date), parse(end_date))
#                 if result:
#                     return True

#     return False