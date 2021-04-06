from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from Tracker.views import HomeView, ProductView, SearchView, DiffView
from Tracker.models import Item

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['']

    def location(self, item):
        return item

sitemaps = {
    'static': StaticViewSitemap,
    'products': GenericSitemap({'queryset': Item.objects.all()}, priority=0.6),
}


urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('diff/', DiffView.as_view(), name='diff-view'), # view all products that have a previous price
    path('product/<slug:slug>/', ProductView.as_view(), name='product-view'),
    path('search/', SearchView.as_view(), name='search-view'),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'UnrealTracker AdminCP'
admin.site.site_title = 'UnrealTracker AdminCP'

handler403 = 'Tracker.views.permission_denied_403'
handler404 = 'Tracker.views.not_found_404'
handler500 = 'Tracker.views.server_error_500'