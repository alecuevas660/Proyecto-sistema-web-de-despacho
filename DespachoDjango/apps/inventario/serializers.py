from rest_framework import serializers
from apps.inventario.models import Product, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source="categoria")
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'