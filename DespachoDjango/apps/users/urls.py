from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import UserListView

app_name = 'users'

urlpatterns = [
    # Redirección de /accounts/ a home
    path('', RedirectView.as_view(pattern_name='home:home'), name='users_home'),
    
    # Clientes
    path('clients/', UserListView.as_view(), {'user_type': 'clients'}, name='client_list'),
    path('clients/create/', views.UserCreateView.as_view(
        extra_context={'user_type': 'client', 'title': 'Nuevo Cliente'}
    ), name='create_client'),
    
    # Empleados
    path('employees/', UserListView.as_view(), {'user_type': 'employees'}, name='employee_list'),
    path('employees/create/', views.UserCreateView.as_view(
        extra_context={'user_type': 'employee', 'title': 'Nuevo Empleado'}
    ), name='create_employee'),
    
    # Operaciones comunes
    path('clients/<uuid:pk>/update/', views.UserUpdateView.as_view(
        extra_context={'user_type': 'client'}
    ), name='update_client'),
    path('employees/<uuid:pk>/update/', views.UserUpdateView.as_view(
        extra_context={'user_type': 'employee'}
    ), name='update_employee'),
    
    path('clients/<uuid:pk>/detail/', views.UserDetailView.as_view(
        extra_context={'user_type': 'client'}
    ), name='detail_client'),
    path('employees/<uuid:pk>/detail/', views.UserDetailView.as_view(
        extra_context={'user_type': 'employee'}
    ), name='detail_employee'),
] 