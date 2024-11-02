from django.shortcuts import render

# Create your views here.

def editar_productos(request, id):
    
    return render(request, 'editar_productos.html')