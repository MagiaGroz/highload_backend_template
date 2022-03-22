import uuid

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(blank=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL,
                                 null=True)
    executor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    priority = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE,
                                null=True)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.created_at} {self.status}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
