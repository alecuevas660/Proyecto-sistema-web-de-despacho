from django.shortcuts import render

# Create your views here.
# mi_aplicacion/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

# Listar usuarios
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'templates/listar_usuarios.html', {'usuarios': usuarios})

# Crear usuario
def crear_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('listar_usuarios')
    else:
        form = UserCreationForm()
    return render(request, 'crear_usuario.html', {'form': form})

# Actualizar usuario
def actualizar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('listar_usuarios')
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, 'actualizar_usuario.html', {'form': form})

# Eliminar usuario
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('listar_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})
