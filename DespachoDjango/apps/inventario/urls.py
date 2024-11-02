from rest_framework import viewsets, permissions
from inventario.models import Product
from inventario.serializers import ProductSerializer
from apps.inventario.views import editar_productos
from django.urls import path

urlpatterns = [
    path('editar-productos/<id>/',editar_productos, name="editar_productos"),
]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]