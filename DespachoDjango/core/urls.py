from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.home.urls', namespace='home')),
    path('admin/', admin.site.urls),
    path('inventario/', include('apps.inventario.urls', namespace='inventario')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
