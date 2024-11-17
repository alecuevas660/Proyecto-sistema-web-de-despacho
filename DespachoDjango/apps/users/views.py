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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def is_admin_or_employee(user):
    """Verifica si el usuario es admin o empleado con permisos de staff"""
    return user.is_authenticated and (user.is_admin or (user.is_employee and user.is_staff))

class BaseUserView(LoginRequiredMixin, UserPassesTestMixin):
    """Vista base para la gestión de usuarios"""
    model = User
    
    def test_func(self):
        return is_admin_or_employee(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, 'No tiene permisos para acceder a esta sección.')
        return redirect('home')  # Asegúrate de tener definida esta URL

class UsersListView(BaseUserView, ListView):
    """Vista para listar usuarios según su tipo"""
    template_name = 'auth/usuarios/lista.html'
    context_object_name = 'users'
    paginate_by = 6  # Máximo 6 usuarios por página

    def get_queryset(self):
        user_type = self.kwargs.get('user_type')
        search_query = self.request.GET.get('search', '')
        filter_attribute = self.request.GET.get('filter', '')

        if user_type == 'clients':
            queryset = User.objects.filter(role='client').select_related('cliente_profile')
            if search_query:
                queryset = queryset.filter(
                    Q(nombre__icontains=search_query) |  # Buscamos en el campo 'nombre'
                    Q(email__icontains=search_query) |  # Buscamos en el campo 'email'
                    Q(cliente_profile__nombre_supermercado__icontains=search_query)  # Buscamos en el 'supermercado'
                )
            if filter_attribute:
                if filter_attribute == 'supermercado':
                    queryset = queryset.filter(cliente_profile__nombre_supermercado__icontains=search_query)
                elif filter_attribute == 'estado':
                    queryset = queryset.filter(is_active=True) if search_query.lower() == 'activo' else queryset.filter(is_active=False)

        elif user_type == 'employees':
            queryset = User.objects.filter(role='employee').select_related('employee_profile')
            if search_query:
                queryset = queryset.filter(
                    Q(nombre__icontains=search_query) |  # Buscamos en el campo 'nombre'
                    Q(email__icontains=search_query) |  # Buscamos en el campo 'email'
                    Q(employee_profile__cargo__icontains=search_query)  # Buscamos en el 'cargo'
                )
            if filter_attribute:
                if filter_attribute == 'cargo':
                    queryset = queryset.filter(employee_profile__cargo__icontains=search_query)
                elif filter_attribute == 'estado':
                    queryset = queryset.filter(is_active=True) if search_query.lower() == 'activo' else queryset.filter(is_active=False)

        else:
            queryset = User.objects.none()  # En caso de un tipo no válido

        return queryset.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Paginación
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context.update({
            'user_type': self.kwargs.get('user_type'),
            'users': users,
            'search_query': self.request.GET.get('search', ''),
            'filter_attribute': self.request.GET.get('filter', ''),
            'title': 'Clientes' if self.kwargs.get('user_type') == 'clients' else 'Empleados',
        })
        return context


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
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
        if user_type == 'client':
            return reverse_lazy('users:client_list')
        elif user_type == 'employee':
            return reverse_lazy('users:employee_list')
        return reverse_lazy('users:user_list')  # fallback
    
    def get_form_class(self):
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
        return ClienteForm if user_type == 'client' else EmployeeForm
    
    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
            user.role = 'client' if user_type == 'client' else 'employee'
            user.save()  # Guardamos primero el usuario
            
            # Guardamos el formulario completo (esto creará el perfil)
            form.save()
            
            messages.success(
                self.request,
                f'{"Cliente" if user_type == "client" else "Empleado"} {user.get_full_name()} creado exitosamente.'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear usuario: {str(e)}')
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
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
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
        return reverse_lazy(f'users:{user_type}_list')
    
    def get_form_class(self):
        user = self.get_object()
        return ClienteUpdateForm if user.is_client else EmployeeUpdateForm
    
    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(
                self.request,
                f'Usuario {user.get_full_name()} actualizado exitosamente.'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar usuario: {str(e)}')
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
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
        user_type = self.kwargs.get('user_type') or self.extra_context.get('user_type')
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
