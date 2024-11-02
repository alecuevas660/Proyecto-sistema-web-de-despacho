from rest_framework import serializers
from inventario.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'price', 'created_at', 'updated_at'
        read_only_fields = 'id', 'created_at', 'updated_at'