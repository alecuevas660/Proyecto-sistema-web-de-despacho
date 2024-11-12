from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('apps.home.urls', 'home'), namespace='home')),
    path('admin/', admin.site.urls),
    path('inventario/', include(('apps.inventario.urls', 'inventario'), namespace='inventario')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('ordenes/', include(('apps.ordenes.urls', 'ordenes'), namespace='ordenes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
