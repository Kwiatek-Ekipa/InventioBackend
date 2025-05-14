from django.core.management import BaseCommand
from hardware.models import Brand


class Command(BaseCommand):

    def handle(self, *args, **options):
        brand_names = [
            "Dell",
            "HP",
            "Lenovo",
            "Asus",
            "Acer",
            "Apple",
            "MSI",
            "Gigabyte"
        ]

        existing_brands = Brand.objects.filter(name__in=brand_names)
        existing_names = set(brand.name for brand in existing_brands)

        missing_names = [name for name in brand_names if name not in existing_names]

        if not missing_names:
            print("All brands have already been added.")
            return

        for name in missing_names:
            Brand.objects.create(name=name)
            print(self.style.SUCCESS(f"Added brand: {name}."))