from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Like


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "order")
    ordering = ("order",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "get_color", "get_size", "get_material", "is_on_sale", "rating")
    list_filter = ("category", "is_on_sale", "color_choice", "size_choice", "material_choice")
    search_fields = ("name", "custom_color", "custom_size", "custom_material")
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("category", "name", "slug", "price")
        }),
        ("Xususiyatlar", {
            "fields": (
                ("color_choice", "custom_color"),
                ("size_choice", "custom_size"),
                ("material_choice", "custom_material"),
                "is_on_sale"
            )
        }),
        ("Qo‘shimcha", {
            "fields": ("rating",)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "user_identifier", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "text", "user_identifier")
    readonly_fields = ("created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("product", "user_identifier", "created_at")
    search_fields = ("product__name", "user_identifier")
    readonly_fields = ("created_at",)
