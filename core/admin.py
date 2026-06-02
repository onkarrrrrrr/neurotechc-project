from django.contrib import admin

from .models import Appointment, Service

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'company', 'service', 'status', 'created_at')
    list_filter = ('service', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'company')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'sort_order', 'is_featured', 'is_active', 'updated_at')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('title', 'slug', 'summary', 'details')
    prepopulated_fields = {'slug': ('title',)}
