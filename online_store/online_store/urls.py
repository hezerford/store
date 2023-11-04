from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('shop.urls')),
    path('api/', include('api.urls')),
    path('account/', include('accounts.urls')),
    path('cart/', include('carts.urls')),
    path('profile/', include('profiles.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)