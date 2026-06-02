from django.db import migrations, models


def seed_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')

    services = [
        {
            'title': 'IP, Subsystem, SOC Verification',
            'slug': 'asic-verification',
            'badge': 'Core Service',
            'summary': 'Comprehensive functional verification at IP, subsystem, and SoC levels using SystemVerilog, UVM, and formal verification.',
            'details': 'Achieving first-pass silicon success requires rigorous, uncompromising verification. We deploy advanced methodologies to expose critical corner-case bugs before tape-out, reducing re-spin risk and schedule slippage.\n\nThe service covers verification planning, environment development, constrained-random testing, and sign-off support for complex SoCs.',
            'highlights': 'IP-level verification for complex interfaces\nSubsystem integration and scoreboarding\nSoC-level boot, reset, and power-aware validation',
            'cta_label': 'Request Consultation',
            'sort_order': 1,
            'is_featured': True,
        },
        {
            'title': 'RTL Design',
            'slug': 'rtl-design',
            'badge': 'Core Service',
            'summary': 'Micro-architecture definition and RTL coding in Verilog, SystemVerilog, or VHDL with a focus on performance, power, and area.',
            'details': 'We turn architectural intent into synthesizable RTL with a strong emphasis on maintainability and design correctness. Each block is designed for integration, verification, and implementation success.',
            'highlights': 'Micro-architecture definition\nClean, CDC-safe RTL coding\nPower-aware and timing-conscious implementation',
            'cta_label': 'Request Consultation',
            'sort_order': 2,
        },
        {
            'title': 'FPGA Prototyping',
            'slug': 'fpga-prototyping',
            'badge': 'Hardware Service',
            'summary': 'Mapping complex ASICs to FPGA platforms for early software development, hardware validation, and system bring-up.',
            'details': 'FPGA prototyping enables shift-left validation and provides a practical hardware target long before silicon is available. We handle partitioning, timing closure, and bring-up support.',
            'highlights': 'Multi-FPGA partitioning\nMemory modeling and interface adaptation\nBring-up and debugging support',
            'cta_label': 'Request Consultation',
            'sort_order': 3,
        },
        {
            'title': 'Functional Coverage',
            'slug': 'functional-coverage',
            'badge': 'Specialty Service',
            'summary': 'Coverage models, assertions, and tracking tools to prove that the verification plan has been fully executed.',
            'details': 'Coverage closure is where verification becomes measurable. We build targeted models and analysis flows that make gaps visible and actionable.',
            'highlights': 'Test plan mapping\nAssertion development\nCoverage closure and sign-off support',
            'cta_label': 'Request Consultation',
            'sort_order': 4,
        },
        {
            'title': 'UVM Testbench Dev',
            'slug': 'uvm-testbench',
            'badge': 'Specialty Service',
            'summary': 'Highly modular, scalable, and reusable UVM testbenches that support block, subsystem, and SoC verification.',
            'details': 'We architect UVM environments with strong reuse, clean layering, and verification assets that scale from a single IP block to a complex chip-level environment.',
            'highlights': 'Agent and sequencer development\nReference models and scoreboards\nRAL integration and vertical reuse',
            'cta_label': 'Request Consultation',
            'sort_order': 5,
        },
        {
            'title': 'Embedded Systems',
            'slug': 'embedded-systems',
            'badge': 'Software Service',
            'summary': 'Firmware, bootloader, and driver development to bring custom silicon to life.',
            'details': 'Hardware is only useful with robust software. We develop bare-metal firmware, diagnostic suites, and low-level drivers that exercise the underlying RTL efficiently.',
            'highlights': 'Boot ROM and bootloaders\nBare-metal drivers\nPre-silicon software and diagnostics',
            'cta_label': 'Request Consultation',
            'sort_order': 6,
        },
        {
            'title': 'General Consulting',
            'slug': 'general-consulting',
            'badge': 'Advisory',
            'summary': 'Flexible technical consulting for architecture reviews, verification strategy, and project planning.',
            'details': 'Use this service when you need senior engineering guidance without committing to a full project engagement. We can help shape the problem, the plan, and the execution model.',
            'highlights': 'Architecture reviews\nVerification strategy\nProject scoping and execution planning',
            'cta_label': 'Request Consultation',
            'sort_order': 7,
        },
    ]

    for service_data in services:
        Service.objects.update_or_create(
            slug=service_data['slug'],
            defaults=service_data,
        )


def unseed_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    Service.objects.filter(slug__in=[
        'asic-verification',
        'rtl-design',
        'fpga-prototyping',
        'functional-coverage',
        'uvm-testbench',
        'embedded-systems',
        'general-consulting',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True)),
                ('badge', models.CharField(blank=True, max_length=120)),
                ('summary', models.TextField()),
                ('details', models.TextField(blank=True)),
                ('highlights', models.TextField(blank=True)),
                ('cta_label', models.CharField(default='Request Consultation', max_length=80)),
                ('cta_url', models.CharField(blank=True, max_length=255)),
                ('icon_svg', models.TextField(blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
            },
        ),
        migrations.RunPython(seed_services, unseed_services),
    ]