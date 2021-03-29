from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View, ListView
from django.core.exceptions import PermissionDenied

from .models import Item

class HomeView(ListView):
    template_name = 'home/index.html'
    queryset = Item.objects.all()
    context_object_name = 'items'
    paginate_by = 100



def permission_denied_403(request, exception=None):
    return render(request, 'error_pages/403.html', status=403)

def not_found_404(request, exception=None):
    return render(request, 'error_pages/404.html', status=404)

def server_error_500(request, exception=None):
    return render(request, 'error_pages/500.html', status=500)