import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

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
    address = models.CharField(max_length=100, blank=True, null=True)
    kitchen = models.CharField(max_length=100, blank=True, null=True)
    average_check = models.CharField(max_length=100, blank=True, null=True)
    place_quantity = models.IntegerField(null=True)
    work_time = models.CharField(max_length=100, blank=True, null=True)
    has_karaoke = models.BooleanField(default=False)
    has_smoking_area = models.BooleanField(default=False)
    parking_area = models.CharField(max_length=100, blank=True, null=True)

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
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.created_at} {self.status}'


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
