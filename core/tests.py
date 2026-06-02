from django.test import TestCase

from .forms import AppointmentForm, ServiceForm
from .models import Service


class ServiceCrudTests(TestCase):
	def test_service_save_generates_slug(self):
		service = Service.objects.create(
			title='Custom Verification Review',
			summary='A short summary for a new service.',
		)

		self.assertEqual(service.slug, 'custom-verification-review')

	def test_appointment_form_uses_service_slugs(self):
		service = Service.objects.create(
			title='Board Bring-Up',
			slug='board-bring-up',
			summary='Bring-up support for new boards and prototypes.',
		)

		form = AppointmentForm()
		self.assertIn((service.slug, service.title), list(form.fields['service'].choices))

	def test_service_form_accepts_model_fields(self):
		form = ServiceForm(data={
			'title': 'Signal Integrity Review',
			'slug': 'signal-integrity-review',
			'badge': '',
			'summary': 'Service summary',
			'details': 'Long form details',
			'highlights': 'One\nTwo',
			'cta_label': 'Request Consultation',
			'cta_url': '',
			'icon_svg': '',
			'sort_order': 10,
			'is_featured': False,
			'is_active': True,
		})

		self.assertTrue(form.is_valid())
