
import json
from django import template

register = template.Library()

@register.filter(name='parsejson')
def parsejson(str, arg):
    new_str = json.loads(str.replace('\'','"'))
    return new_str[arg]


@register.filter(name='haschangedprice')
def haschangedprice(str):
    return True