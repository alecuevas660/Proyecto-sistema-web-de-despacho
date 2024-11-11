
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.home.views import HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('reportes/', views.reporte_view, name='reportes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
