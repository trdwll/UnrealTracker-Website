from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View, ListView
from django.core.exceptions import PermissionDenied
from django.db.models import Q 

import json


from .models import Item

class HomeView(ListView):
    template_name = 'home/index.html'
    queryset = Item.objects.all()
    context_object_name = 'items'
    paginate_by = 100


class ProductView(View):
    template_name = 'product/index.html'

    def get(self, request, slug):
        product = Item.objects.filter(slug=slug).first()
        try:
            price_data = json.loads(product.current_price.replace('\'','"'))
            previous_prices = ''
            price = price_data['price']
            last_updated = price_data['date']
            if product.previous_prices:
                previous_prices_data = product.previous_prices.replace('\'','"')
                previous_prices = json.loads(previous_prices_data)

            data = {'product': product, 'price': price, 'last_updated': last_updated, 'previous_prices': previous_prices}
        except json.decoder.JSONDecodeError:
            data = {'product': product}
        return render(request, self.template_name, data)


class SearchView(ListView):
    template_name = 'search/index.html'
    context_object_name = 'items'
    paginate_by = 100

    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query)# | Q(category__title__icontains=query)
        )
        return object_list


class DiffView(ListView):
    template_name = 'diff/index.html'
    context_object_name = 'items'
    paginate_by = 100

    def get_queryset(self):
        return Item.objects.exclude(previous_prices='')


def permission_denied_403(request, exception=None):
    return render(request, 'error_pages/403.html', status=403)

def not_found_404(request, exception=None):
    return render(request, 'error_pages/404.html', status=404)

def server_error_500(request, exception=None):
    return render(request, 'error_pages/500.html', status=500)