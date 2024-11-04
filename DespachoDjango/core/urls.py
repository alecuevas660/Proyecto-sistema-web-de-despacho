
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.home.views import HomeView
from apps.email_service.api.views import EmailAPIView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('send-email', EmailAPIView.as_view(), name='send-email'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    
