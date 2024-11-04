from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.users.views import logout_view

urlpatterns = [
    path('', include('apps.home.urls', namespace='home')),
    path('admin/', admin.site.urls),
    path('inventario/', include('apps.inventario.urls', namespace='inventario')),
    
    # Rutas de autenticación y usuarios
    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Rutas de usuarios (más limpias)
    path('accounts/', include(('apps.users.urls', 'users'), namespace='users')),
    
    # Otras rutas de autenticación
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html'
    ), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Rutas de usuarios
    path('accounts/users/', include(('apps.users.urls', 'users'), namespace='users')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
