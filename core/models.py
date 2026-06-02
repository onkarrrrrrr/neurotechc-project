from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    badge = models.CharField(max_length=120, blank=True)
    summary = models.TextField()
    details = models.TextField(blank=True)
    highlights = models.TextField(blank=True)
    cta_label = models.CharField(max_length=80, default='Request Consultation')
    cta_url = models.CharField(max_length=255, blank=True)
    icon_svg = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'service'
            slug = base_slug
            suffix = 2

            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{suffix}'
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def highlight_items(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

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
