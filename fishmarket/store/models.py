from django.db import models
from django.contrib.auth.models import User

class FishCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fish(models.Model):
    category = models.ForeignKey(FishCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='fish/')
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200, default="Guest")
    phone = models.CharField(max_length=20, default="")
    address = models.TextField(default="")
    city = models.CharField(max_length=100, default="")

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fish_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.fish_name
