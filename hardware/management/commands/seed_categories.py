from django.core.management import BaseCommand
from hardware.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_names = [
            "Klawiatury",
            "Komputery stacjonarne",
            "Laptopy",
            "Drukarki",
            "Lodówki",
            "Smartfony",
            "Smart Odkurzacze",
            "Smart Lodówki"
        ]

        existing_categories = Category.objects.filter(name__in=category_names)
        existing_names = set(category.name for category in existing_categories)

        missing_names = [name for name in category_names if name not in existing_names]

        if not missing_names:
            print("All categories have already been added.")
            return

        for name in missing_names:
            Category.objects.create(name=name)
            print(self.style.SUCCESS("Added category: {name}."))
