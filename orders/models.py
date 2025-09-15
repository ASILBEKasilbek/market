from django.db import models
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('delivered', 'Yetkazildi'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order for {self.product.name} by {self.customer_name}"