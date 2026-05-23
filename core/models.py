from django.db import models

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('DV', 'Design Verification'),
        ('RTL', 'RTL Design'),
        ('FPGA', 'FPGA Prototyping'),
        ('UVM', 'UVM Testbench'),
        ('COVERAGE', 'Functional Coverage'),
        ('EMBEDDED', 'Embedded Systems'),
        ('CONSULTING', 'General Consulting'),
    ]
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=200, blank=True)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='NEW')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()}"
