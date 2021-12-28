from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet, ProductViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls))
]
