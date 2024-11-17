from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth import logout
from .models import User, ClienteProfile, EmployeeProfile
from .forms import ClienteForm, EmployeeForm, ClienteUpdateForm, EmployeeUpdateForm
from .forms import ClienteForm, EmployeeForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse


def is_admin_or_employee(user):
    """Verifica si el usuario es admin o empleado con permisos de staff"""
    return user.is_authenticated and (user.is_admin or (user.is_employee and user.is_staff))


class BaseUserView(LoginRequiredMixin, UserPassesTestMixin):
    """Vista base para la gestión de usuarios"""
    model = User

    def test_func(self):
        return is_admin_or_employee(self.request.user)

    def handle_no_permission(self):
        messages.error(
            self.request, 'No tiene permisos para acceder a esta sección.')
        return redirect('home')  # Asegúrate de tener definida esta URL


class UserListView(BaseUserView, ListView):
    """Vista para listar usuarios según su tipo"""
    template_name = 'auth/usuarios/lista.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type', 'all')
        print(f"User type: {user_type}")

        if user_type == 'clients':
            queryset = queryset.filter(role='client')
        elif user_type == 'employees':
            queryset = queryset.filter(role='employee')

        print(f"Query count: {queryset.count()}")
        return queryset.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type', 'all')

        context.update({
            'user_type': user_type,
            'search_query': self.request.GET.get('search', ''),
            'title': 'Clientes' if user_type == 'clients' else 'Empleados'
        })
        print(f"Context: {context}")
        return context


class UserCreateView(BaseUserView, CreateView):
    """Vista para crear nuevos usuarios"""
    template_name = 'auth/usuarios/form.html'

    def get_success_url(self):
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        if user_type == 'client':
            return reverse_lazy('users:client_list')
        elif user_type == 'employee':
            return reverse_lazy('users:employee_list')
        return reverse_lazy('users:user_list')  # fallback

    def get_form_class(self):
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        return ClienteForm if user_type == 'client' else EmployeeForm

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user_type = self.kwargs.get(
                'user_type') or self.extra_context.get('user_type')
            user.role = 'client' if user_type == 'client' else 'employee'
            user.is_active = False
            user.verification_token = get_random_string(32)
            user.save()  # Guardamos primero el usuario

            """ Enviar el correo de verificacion """
            current_site = get_current_site(self.request)
            verification_url = reverse('users:verify_email', args=[
                                       user.verification_token])
            full_verification_url = f"http://{
                current_site.domain}{verification_url}"

            send_mail(
                'Verificacion de correo electronico',
                f'Hola {user.get_full_name()},\n\nPor favor, confirma tu correo electrónico haciendo clic en el siguiente enlace: {
                    full_verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            # Guardamos el formulario completo (esto creará el perfil)
            form.save()

            messages.success(
                self.request,
                f'{"Cliente" if user_type == "client" else "Empleado"} {
                    user.get_full_name()} creado exitosamente.'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear usuario: {str(e)}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        context.update({
            'title': 'Crear Cliente' if user_type == 'client' else 'Crear Empleado',
            'is_update': False,
            'user_type': user_type,  # Agregamos user_type al contexto
            'cancel_url': reverse_lazy(f'users:{"client" if user_type == "client" else "employee"}_list')
        })
        return context


class UserUpdateView(BaseUserView, UpdateView):
    """Vista para actualizar usuarios existentes"""
    template_name = 'auth/usuarios/form.html'

    def get_success_url(self):
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        return reverse_lazy(f'users:{user_type}_list')

    def get_form_class(self):
        user = self.get_object()

        return ClienteUpdateForm if user.is_client else EmployeeUpdateForm

        return ClienteForm if user.is_client else EmployeeForm

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(
                self.request,
                f'Usuario {user.get_full_name()} actualizado exitosamente.'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request, f'Error al actualizar usuario: {str(e)}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        context.update({
            'title': f'Actualizar {"Cliente" if user_type == "client" else "Empleado"}',
            'is_update': True,
            'cancel_url': reverse_lazy(f'users:{user_type}_list')
        })
        return context


class UserDetailView(BaseUserView, DetailView):
    """Vista para ver detalles de un usuario"""
    template_name = 'auth/usuarios/detalle.html'
    context_object_name = 'user_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_type = self.kwargs.get(
            'user_type') or self.extra_context.get('user_type')
        context.update({
            'profile': user.cliente_profile if user.is_client else user.employee_profile,
            'back_url': reverse_lazy(f'users:{user_type}_list')
        })
        return context


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('login')
    elif request.method == 'GET':
        return render(request, 'auth/logout.html')
    else:
        messages.error(request, 'Método no permitido')
        return redirect('home:home')


def user_form_view(request, pk=None):
    user = get_object_or_404(User, pk=pk) if pk else None

    if user:
        # Actualización
        if user.is_client:
            form_class = ClienteUpdateForm
        else:
            form_class = EmployeeUpdateForm
    else:
        # Creación
        if request.GET.get('type') == 'client':
            form_class = ClienteForm
        else:
            form_class = EmployeeForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=form.instance.pk)
    else:
        form = form_class(instance=user)

    context = {
        'form': form,
        'is_update': bool(user),
        'title': 'Actualizar Usuario' if user else 'Crear Usuario',
        'cancel_url': reverse('user_list')
    }
    return render(request, 'auth/usuarios/form.html', context)


def verify_email(request, token):
    try:
        user = get_object_or_404(User, verification_token=token)
        user.is_verified = True
        user.is_active = True
        """ Elimina el token despues de la verificación"""
        user.verification_token = None
        user.save()

        messages.success(
            request, '¡Tu correo ha sido verificado con exito! Ahora puedes iniciar sesion')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(
            request, 'El enlace de verificación no es valido o ha expirado')
        return redirect('home')
