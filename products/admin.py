from django.contrib import admin
from products.models import (
    Category,
    Product,
    ProductImage,
    ColorVariant,
    SizeVariant,
    Coupon,
)

# Register your models here.
admin.site.register(Coupon)
admin.site.register(Category)


# ==========>start of modifying admin panel to add "ProductImage" table under "Product" table<=========
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]


admin.site.register(Product, ProductAdmin)
# ==========>ending of modifying admin panel to add "ProductImage" table under "Product" table<=========

admin.site.register(ProductImage)


# ===========> start of registering in two (02) new ways with "list_filter" options
# 01
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ["color_name", "price"]
    list_filter = ("color_name", "price")


admin.site.register(ColorVariant, ColorVariantAdmin)

# 02
@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ["size_name", "price"]
    model = SizeVariant


# ===========> end of registering in two new ways with "list_filter" options
