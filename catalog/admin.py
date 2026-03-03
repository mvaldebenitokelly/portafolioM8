from django.contrib import admin
from .models import Category, Product, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "active")
    list_filter = ("active", "category")
    search_fields = ("name", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "email", "subject", "status")
    list_filter = ("status", "created_at")
    search_fields = ("email", "subject", "message")
    readonly_fields = ("created_at",)
