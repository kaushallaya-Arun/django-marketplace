from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager

class User(AbstractUser):
    # Add custom fields  
    #based on your database schema
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)  
    #role = models.CharField(max_length=10, choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('admin', 'Admin')], default='buyer')
    groups = models.ManyToManyField('auth.Group', related_name='store_users')  # Add related_name here
    user_permissions = models.ManyToManyField('auth.Permission', related_name='store_users')  # Add related_name here


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)  

    stock = models.IntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)  

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()  

    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  

    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
