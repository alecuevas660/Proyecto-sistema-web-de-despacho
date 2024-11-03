from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm

# Vista para listar usuarios
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, '', {'usuarios': usuarios})

# Vista para crear un usuario
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = CustomUserCreationForm()
    return render(request, '', {'form': form})

# Vista para actualizar un usuario
def actualizar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, '', {'form': form, 'usuario': usuario})

# Vista para eliminar un usuario
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('')
    return render(request, '', {'usuario': usuario})
