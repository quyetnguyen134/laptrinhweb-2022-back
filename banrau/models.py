from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, null=False)

    def __str__(self):
        return "Danh mục " + self.name


class Product(models.Model):
    name = models.CharField(max_length=128, null=False)
    desc = models.CharField(max_length=1024, null=False)
    price = models.IntegerField(null=False)
    image = models.CharField(max_length=255, null=False)
    category = models.ManyToManyField(Category)
