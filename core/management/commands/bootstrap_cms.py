from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from cms.api import add_plugin, create_page
from cms.models import Page
from djangocms_text.cms_plugins import TextPlugin


CMS_PAGE_DEFINITIONS = [
    {
        'reverse_id': 'home',
        'title': 'Home',
        'slug': '/',
        'template': 'cms/home.html',
        'homepage': True,
        'placeholders': {
            'hero': '<h1 class="text-6xl md:text-7xl lg:text-8xl font-heading font-bold mb-6 leading-[1.1] tracking-tight">ARM SoC Expert<br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Verification.</span></h1><p class="text-xl text-gray-300 mb-6 max-w-2xl font-sans font-light leading-relaxed">Delivering quick testbench bring-up environments and flows. Specialized in Cortex-R & Cortex-A verification for zero-defect silicon.</p>',
            'content': '<h2 class="text-4xl md:text-5xl font-heading font-bold mb-6 tracking-tight">Who We Are</h2><p class="text-gray-400 text-lg font-light leading-relaxed">Use the CMS toolbar to edit this section visually. The homepage can be updated without touching templates.</p>',
        },
    },
    {
        'reverse_id': 'services',
        'title': 'Services',
        'slug': 'services',
        'template': 'cms/services.html',
        'placeholders': {
            'services_intro': '<h1 class="text-4xl md:text-5xl font-heading font-bold mb-6 tracking-tight text-black dark:text-white">Services you can edit from the page editor.</h1><p class="text-[#555] dark:text-gray-400 text-lg">The cards below stay data-driven from your existing services model, while this intro text stays editable in the CMS.</p>',
        },
    },
    {
        'reverse_id': 'about',
        'title': 'About Us',
        'slug': 'about',
        'template': 'cms/page.html',
        'placeholders': {
            'content': '<h1>About Neurotech Circuits</h1><p>Edit this page visually from the CMS frontend or the admin page editor.</p>',
        },
    },
    {
        'reverse_id': 'product',
        'title': 'Product',
        'slug': 'product',
        'template': 'cms/page.html',
        'placeholders': {
            'content': '<h1>Product</h1><p>This content is now managed through django CMS.</p>',
        },
    },
    {
        'reverse_id': 'methodology',
        'title': 'Methodology',
        'slug': 'methodology',
        'template': 'cms/page.html',
        'placeholders': {
            'content': '<h1>Methodology</h1><p>Describe your workflow, milestones, and delivery model here.</p>',
        },
    },
    {
        'reverse_id': 'contact',
        'title': 'Contact',
        'slug': 'contact',
        'template': 'cms/contact.html',
        'placeholders': {
            'contact_intro': '<h1>Contact Neurotech Circuits</h1><p>Use the form to submit an enquiry. The surrounding page copy is editable in CMS.</p>',
        },
    },
]


from django.db import transaction

class Command(BaseCommand):
    help = 'Create the default CMS pages if they do not already exist.'

    def handle(self, *args, **options):
        site = Site.objects.get_current()
        author = get_user_model().objects.filter(is_superuser=True).order_by('id').first()

        created = 0

        for definition in CMS_PAGE_DEFINITIONS:
            with transaction.atomic():
                page = Page.objects.filter(reverse_id=definition['reverse_id']).first()
                if page is None:
                    page_kwargs = {
                        'template': definition['template'],
                        'language': 'en',
                        'site': site,
                        'slug': definition['slug'],
                        'reverse_id': definition['reverse_id'],
                        'in_navigation': True,
                    }
                    if author is not None:
                        page_kwargs['created_by'] = author

                    page = create_page(definition['title'], **page_kwargs)
                    created += 1

                if definition.get('homepage'):
                    page.set_as_homepage(user=author)

                for placeholder in page.get_placeholders('en'):
                    html = definition.get('placeholders', {}).get(placeholder.slot)
                    if html and not placeholder.get_plugins('en').exists():
                        add_plugin(placeholder, TextPlugin, 'en', body=html)

                try:
                    page.publish('en')
                except Exception:
                    # If the CMS version uses versioning internally, the page is still created.
                    pass

        self.stdout.write(self.style.SUCCESS(f'Bootstrap complete. Created {created} CMS page(s).'))

