from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import AppointmentForm
from .db import (
    save_appointment_to_mongodb,
    get_all_appointments,
    update_appointment,
    delete_appointment
)

def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def service_detail(request, service_slug):
    return render(request, 'service_detail.html', {'slug': service_slug})

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
    if request.method == 'POST':
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
        
    try:
        appointments = get_all_appointments()
    except Exception as e:
        appointments = []
        messages.error(request, f'Failed to retrieve appointments from MongoDB: {e}')
        
    return render(request, 'admin/dashboard.html', {'appointments': appointments})

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
