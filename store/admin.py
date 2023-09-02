from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

from tags.models import TaggedItem
from django.db.models import Count


# Registering Models
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))


# admin.site.register(models.Product)
# for creating columns in Product class
class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low"),
            (">=10", "OK"),
        ]

    def queryset(self, request, queryset=QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class TagInline(GenericTabularInline):
    autocomplete_fields = ["tag"]
    model = TaggedItem


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title", "description"]
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    inlines = [TagInline]
    prepopulated_fields = {"slug": ["title"]}
    exclude = ["promotions"]
    list_display = [
        "title",
        "unit_price",
        "inventory",
        "inventory_status",
        "collection_title",
    ]
    list_editable = ("unit_price",)
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 10

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    list_select_related = ["collection"]

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            level="success",
        )

    clear_inventory.short_description = "Clear inventory"


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ("membership",)
    ordering = ["first_name", "last_name"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer"]
    list_per_page = 10
    inlines = [OrderItemInline]
    autocomplete_fields = ["customer"]
