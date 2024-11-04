from django.urls import path
from .views import HomeView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # Si quieres mantener el index como página separada:
    # path('', IndexView.as_view(), name='index'),
    # path('dashboard/', HomeView.as_view(), name='dashboard'),
]
