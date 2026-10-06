from django.contrib import admin

from .models import (
    Audience,
    Company,
    FAQ,
    LegalPage,
    OrderFormField,
    Package,
    SiteContent,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email_info", "phone_sales")


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("key",)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency", "featured", "sort_order")
    list_editable = ("sort_order", "featured")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "sort_order")
    list_editable = ("sort_order",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "slug", "sort_order")
    list_editable = ("sort_order",)


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(OrderFormField)
class OrderFormFieldAdmin(admin.ModelAdmin):
    list_display = ("label", "field_id", "field_type", "required", "sort_order")
    list_editable = ("sort_order",)
