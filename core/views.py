from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404

from .forms import AppointmentForm, ServiceForm
from .models import Service
from .db import (
    save_appointment_to_mongodb,
    get_all_appointments,
    update_appointment,
    delete_appointment
)


LEGACY_SERVICE_LABELS = {
    'DV': 'Design Verification',
    'RTL': 'RTL Design',
    'FPGA': 'FPGA Prototyping',
    'UVM': 'UVM Testbench',
    'COVERAGE': 'Functional Coverage',
    'EMBEDDED': 'Embedded Systems',
    'CONSULTING': 'General Consulting',
    'asic-verification': 'IP, Subsystem, SOC Verification',
    'rtl-design': 'RTL Design',
    'fpga-prototyping': 'FPGA Prototyping',
    'functional-coverage': 'Functional Coverage',
    'uvm-testbench': 'UVM Testbench Dev',
    'embedded-systems': 'Embedded Systems',
}


def get_service_label(value):
    service = Service.objects.filter(slug=value, is_active=True).first()
    if service:
        return service.title

    return LEGACY_SERVICE_LABELS.get(value, value)

def home(request):
    return render(request, 'home.html')

def services(request):
    services = Service.objects.filter(is_active=True).order_by('sort_order', 'title')
    return render(request, 'services.html', {'services': services})

def service_detail(request, service_slug):
    service = Service.objects.filter(slug=service_slug, is_active=True).first()
    return render(request, 'service_detail.html', {'service': service, 'slug': service_slug})

def domain_detail(request, domain_slug):
    return render(request, 'domain_detail.html', {'slug': domain_slug})

def product(request):
    return render(request, 'product.html')

def methodology(request):
    return render(request, 'methodology.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                save_appointment_to_mongodb(form.cleaned_data)
                messages.success(request, 'Your appointment request has been submitted successfully. We will contact you soon.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'Database Error: Could not save your submission. Details: {e}')
    else:
        form = AppointmentForm()
    
    return render(request, 'contact.html', {'form': form})

@staff_member_required(login_url='admin_login')
def admin_dashboard(request):
    service_form = None
    editing_service = None

    if request.method == 'POST':
        panel = request.POST.get('panel', 'appointments')

        if panel == 'services':
            service_action = request.POST.get('service_action')
            service_id = request.POST.get('service_id')
            editing_service = Service.objects.filter(pk=service_id).first() if service_id else None

            if service_action == 'delete' and editing_service:
                service_name = editing_service.title
                editing_service.delete()
                messages.success(request, f'Service "{service_name}" deleted successfully.')
                return redirect('admin_dashboard')

            service_form = ServiceForm(request.POST, instance=editing_service)
            if service_form.is_valid():
                saved_service = service_form.save()
                if editing_service:
                    messages.success(request, f'Service "{saved_service.title}" updated successfully.')
                else:
                    messages.success(request, f'Service "{saved_service.title}" created successfully.')
                return redirect('admin_dashboard')

            messages.error(request, 'Please correct the errors below and try again.')
        else:
            action = request.POST.get('action')
            appt_id = request.POST.get('appt_id')

            try:
                if action == 'confirm':
                    update_appointment(appt_id, status='CONFIRMED')
                    messages.success(request, 'Appointment status updated to Confirmed.')
                elif action == 'save_note':
                    note_text = request.POST.get('note', '')
                    update_appointment(appt_id, note=note_text)
                    messages.success(request, 'Appointment notes updated.')
                elif action == 'delete':
                    delete_appointment(appt_id)
                    messages.success(request, 'Appointment deleted successfully.')
            except Exception as e:
                messages.error(request, f'Database Error: {e}')

            return redirect('admin_dashboard')

    if request.method == 'GET':
        service_id = request.GET.get('service_id')
        if service_id:
            editing_service = get_object_or_404(Service, pk=service_id)

    if service_form is None:
        service_form = ServiceForm(instance=editing_service)
        
    try:
        appointments = get_all_appointments()
        for appointment in appointments:
            appointment['service_label'] = get_service_label(appointment.get('service', ''))
    except Exception as e:
        appointments = []
        messages.error(request, f'Failed to retrieve appointments from MongoDB: {e}')

    services = Service.objects.all().order_by('sort_order', 'title')

    return render(request, 'admin/dashboard.html', {
        'appointments': appointments,
        'services': services,
        'service_form': service_form,
        'editing_service': editing_service,
    })

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                auth_login(request, user)
                next_url = request.GET.get('next', 'admin_dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Access denied. Only administrators are allowed.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'admin/login.html', {'form': form})

def admin_logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin_login')
