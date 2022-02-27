from django.contrib import admin

from banrau.models import Product, Category


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "categories"]

    def categories(self, obj):
        return ", ".join(str(p.name) for p in obj.category.all())


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["name"]
