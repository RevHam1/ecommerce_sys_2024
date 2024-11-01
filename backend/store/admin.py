from django.contrib import admin
from store.models import (Cart, CartOrder, CartOrderItem, Category, Color,
                          Gallery, Product, Review, Size, Specification, Tax)


class GalleryInline(admin.TabularInline):
    model = Gallery
    # extra = 0


class SpecificationInline(admin.TabularInline):
    model = Specification
    # extra = 0


class SizeInline(admin.TabularInline):
    model = Size
    # extra = 0


class ColorInline(admin.TabularInline):
    model = Color
    # extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'shipping_amount',
                    'stock_qty', 'in_stock', 'vendor', 'featured']
    list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['title']
    inlines = [GalleryInline, SpecificationInline, SizeInline, ColorInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Tax)
