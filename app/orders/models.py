from django.db import models


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL,
                                 null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f'{self.created_at} {self.status}'
