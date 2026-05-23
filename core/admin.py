from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'company', 'service', 'status', 'created_at')
    list_filter = ('service', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'company')
