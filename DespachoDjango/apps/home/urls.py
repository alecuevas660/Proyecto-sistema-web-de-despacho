from django.urls import path
from . import views
from .views import HomeView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
