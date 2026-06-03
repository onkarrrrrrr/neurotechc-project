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
        field_classes = {
            'full_name': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10',
            'email': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10',
            'phone': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10',
            'company': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10',
            'service': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10',
            'message': 'w-full px-4 py-3 rounded border border-[#eaeaea] bg-white text-black focus:outline-none focus:ring-2 focus:ring-black/10 min-h-40',
        }

        for field_name, class_name in field_classes.items():
            self.fields[field_name].widget.attrs['class'] = class_name


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
