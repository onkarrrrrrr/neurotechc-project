from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('domain/<slug:domain_slug>/', views.domain_detail, name='domain_detail'),
    path('services/', views.services, name='services'),
    path('services/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('product/', views.product, name='product'),
    path('methodology/', views.methodology, name='methodology'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
