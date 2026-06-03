from django.urls import path
from . import views

urlpatterns = [
    path('domain/<slug:domain_slug>/', views.domain_detail, name='domain_detail'),
    path('service/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
