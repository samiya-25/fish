from django.db import models

class FishCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fish(models.Model):
    category = models.ForeignKey(FishCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='fish/')
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
