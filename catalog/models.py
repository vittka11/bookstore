from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.title
