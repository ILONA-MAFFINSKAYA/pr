from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    TYPE_CHOICES = (
        ('товар', 'Товар'),
        ('услуга', 'Услуга'),
        ('программное обеспечение', 'Программное обеспечение'),
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='')
    quantity = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    tags = models.CharField(max_length=255)
    article = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    number = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=255)
    description = models.TextField()
    delivery = models.TextField()
    remarks = models.TextField()
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OfferProduct')

class OfferProduct(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."