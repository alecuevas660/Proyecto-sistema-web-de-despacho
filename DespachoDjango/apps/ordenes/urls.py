from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('', views.OrdenDespachoListView.as_view(), name='orden_list'),
    path('crear/', views.OrdenDespachoCreateView.as_view(), name='orden_create'),
    path('<uuid:pk>/', views.OrdenDespachoDetailView.as_view(), name='orden_detail'),
    path('<uuid:pk>/editar/', views.OrdenDespachoUpdateView.as_view(), name='orden_edit'),
    path('<uuid:pk>/eliminar/', views.OrdenDespachoDeleteView.as_view(), name='orden_delete'),
    path('<uuid:pk>/estado/', views.EstadoUpdateView.as_view(), name='estado_update'),
] 