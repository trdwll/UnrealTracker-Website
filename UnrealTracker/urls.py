from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from Tracker.views import HomeView, ProductView

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product-view'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'UnrealTracker AdminCP'
admin.site.site_title = 'UnrealTracker AdminCP'

handler403 = 'Tracker.views.permission_denied_403'
handler404 = 'Tracker.views.not_found_404'
handler500 = 'Tracker.views.server_error_500'