from django import forms

from .models import Service


LEGACY_SERVICE_CHOICES = [
    ('DV', 'Design Verification'),
    ('RTL', 'RTL Design'),
    ('FPGA', 'FPGA Prototyping'),
    ('UVM', 'UVM Testbench'),
    ('COVERAGE', 'Functional Coverage'),
    ('EMBEDDED', 'Embedded Systems'),
    ('CONSULTING', 'General Consulting'),
]


def get_service_choices():
    try:
        services = list(Service.objects.filter(is_active=True).order_by('sort_order', 'title'))
    except Exception:
        return LEGACY_SERVICE_CHOICES

    if not services:
        return LEGACY_SERVICE_CHOICES

    return [(service.slug, service.title) for service in services]

class AppointmentForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    company = forms.CharField(max_length=200, required=False)
    service = forms.ChoiceField(choices=LEGACY_SERVICE_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].choices = get_service_choices()


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title',
            'slug',
            'badge',
            'summary',
            'details',
            'highlights',
            'cta_label',
            'cta_url',
            'icon_svg',
            'sort_order',
            'is_featured',
            'is_active',
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'details': forms.Textarea(attrs={'rows': 8}),
            'highlights': forms.Textarea(attrs={'rows': 5}),
            'icon_svg': forms.Textarea(attrs={'rows': 4}),
        }
