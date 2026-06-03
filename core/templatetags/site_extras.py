from django import template

from core.forms import AppointmentForm
from core.models import Service


register = template.Library()


@register.inclusion_tag('core/partials/service_cards.html')
def service_cards(limit=None):
    services = Service.objects.filter(is_active=True).order_by('sort_order', 'title')
    if limit:
        services = services[:limit]
    return {'services': services}


@register.inclusion_tag('core/partials/contact_form.html', takes_context=True)
def appointment_form(context):
    request = context.get('request')
    initial = {}
    if request is not None:
        service = request.GET.get('service')
        if service:
            initial['service'] = service

    return {
        'form': AppointmentForm(initial=initial),
        'submit_url': '/contact/submit/',
    }
