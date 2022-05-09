from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet, get_products, ProductOwnerViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products/owner', ProductOwnerViewSet)
router.register('orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'products/', get_products, name='get_products')
]
