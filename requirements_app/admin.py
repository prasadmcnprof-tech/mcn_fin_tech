from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import ServiceCategory, Service, CustomerRequest, RequestDocument

admin.site.site_header = "Business Services Admin"
admin.site.site_title = "Service Platform Admin"
admin.site.index_title = "Dashboard"

class RequestDocumentInline(admin.TabularInline):
    model = RequestDocument
    extra = 0
    readonly_fields = ("uploaded_at",)

@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ("request_number", "customer_name", "phone", "service", "status", "payment_status", "created_at")
    list_filter = ()
    search_fields = ("request_number", "customer_name", "phone", "email", "company_name", "service__title")
    list_editable = ("status", "payment_status")
    readonly_fields = ("request_number", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    inlines = [RequestDocumentInline]

@admin.register(RequestDocument)
class RequestDocumentAdmin(admin.ModelAdmin):
    list_display = ("document_name", "customer_request", "uploaded_by", "verified", "uploaded_at")
    list_filter = ()
    search_fields = ("document_name", "customer_request__request_number", "customer_request__customer_name")
    list_editable = ("verified",)
    readonly_fields = ("uploaded_at",)
    date_hierarchy = "uploaded_at"
    ordering = ("-uploaded_at",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "starting_price", "expected_timeline", "is_active")
    list_filter = ()
    search_fields = ("title", "short_description", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order", "title")

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ()
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active")
    list_filter = ()
    search_fields = ("username", "email", "first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
