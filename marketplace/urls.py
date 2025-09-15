from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth URLs (login, logout)
    path('accounts/', include('accounts.urls')),  # Custom accounts URLs (register)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)