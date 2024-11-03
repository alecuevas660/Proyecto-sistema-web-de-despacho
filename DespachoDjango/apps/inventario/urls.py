from django.urls import path, include
from rest_framework import viewsets, permissions
from apps.inventario.models import Product
from apps.inventario.serializers import ProductSerializer
from rest_framework import routers

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

router = routers.DefaultRouter()
router.register('producto', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
