from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_item_cost(self, item):
        return item.product.price * item.quantity

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def create(self, request, *args, **kwargs):
        serializer = OrderItemCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user)
        for order_item in serializer.data:
            order_item['order_id'] = order.id
        order_items = serializer.create(serializer.data)
        print(order.id)
        print(order_items)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

