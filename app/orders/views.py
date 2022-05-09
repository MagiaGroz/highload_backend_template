from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductOwnerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all the products
        for the currently authenticated executor.
        """
        user = self.request.user
        return Product.objects.filter(executor=user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data['executor'] = user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        product = serializer.save()

        return Response(self.serializer_class(product).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)

    def get_item_cost(self, item):
        return item.product.price * item.quantity

    def get_total_cost(self, order):
        return sum(self.get_item_cost(item) for item in order.items.all())

    def create(self, request, *args, **kwargs):
        serializer = OrderItemCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user)
        for order_item in serializer.data:
            order_item['order_id'] = order.id

        serializer.create(serializer.data)
        order.price = self.get_total_cost(order)
        order.save()

        return Response(self.serializer_class(order).data, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def get_products(request):
    category = request.GET.get('category')
    queryset = Product.objects.all()
    if category:
        queryset = queryset.filter(category=category)
    data = list(queryset.values())
    return JsonResponse(data, safe=False)