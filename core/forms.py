from django import forms

class AppointmentForm(forms.Form):
    SERVICE_CHOICES = [
        ('DV', 'Design Verification'),
        ('RTL', 'RTL Design'),
        ('FPGA', 'FPGA Prototyping'),
        ('UVM', 'UVM Testbench'),
        ('COVERAGE', 'Functional Coverage'),
        ('EMBEDDED', 'Embedded Systems'),
        ('CONSULTING', 'General Consulting'),
    ]
    
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    company = forms.CharField(max_length=200, required=False)
    service = forms.ChoiceField(choices=SERVICE_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, required=False)
