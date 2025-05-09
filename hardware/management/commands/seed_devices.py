from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from hardware.models import Device, Brand, Category
from inventio_auth.models import Account, Role
from inventio_auth.enums import RoleEnum
from django.utils.timezone import make_aware
import random


class Command(BaseCommand):
    help = "Seed example devices into the database."

    def handle(self, *args, **options):
        try:
            technician_role = Role.objects.get(name=RoleEnum.TECHNICIAN.value)
            technician = Account.objects.filter(role=technician_role).order_by('id').first()
            if not technician:
                print(self.style.ERROR("No technician account found. Cannot proceed."))
                return
        except ObjectDoesNotExist:
            print(self.style.ERROR("Technician role does not exist. Cannot proceed."))
            return

        devices_to_add = [
            {"model": "Legion Y540", "brand": "Lenovo", "category": "Laptopy"},
            {"model": "S24", "brand": "Apple", "category": "Smartfony"},
            {"model": "DCP-J315W", "brand": "HP", "category": "Drukarki"},
            {"model": "DCP-T720DW", "brand": "HP", "category": "Drukarki"},
            {"model": "K8 Pro", "brand": "Asus", "category": "Klawiatury"},
            {"model": "Super Extra Hiper Max", "brand": "Acer", "category": "Komputery stacjonarne"},
        ]

        now = datetime.now()
        five_years_ago = now.replace(year=now.year - 5)

        for device_data in devices_to_add:
            brand = Brand.objects.filter(name=device_data["brand"]).first()
            category = Category.objects.filter(name=device_data["category"]).first()

            if not brand:
                print(self.style.WARNING(
                    f"Skipping device '{device_data['model']}': Brand is missing."
                    f"Please run seed_brands.py first!"
                ))
                continue
            if not category:
                print(self.style.WARNING(
                    f"Skipping device '{device_data['model']}': Category is missing."
                    f"Please run seed_categories.py first!"
                ))
                continue

            existing = Device.objects.filter(
                model=device_data["model"],
                brand_id=brand,
                category_id=category
            ).exists()

            if existing:
                print(f"Device '{device_data['model']}' already exists. Skipping.")
                continue

            serial_number = f"{device_data['model'].replace(' ', '').upper()}-{random.randint(10000, 99999)}"

            random_added_date = make_aware(five_years_ago + timedelta(
                seconds=random.randint(0, int((now - five_years_ago).total_seconds()))
            ))
            random_year = random.randint(five_years_ago.year, now.year)

            device = Device.objects.create(
                model=device_data["model"],
                brand_id=brand,
                category_id=category,
                year_of_production=random_year,
                added_date=random_added_date,
                added_by=technician,
                serial_number=serial_number
            )
            print(self.style.SUCCESS(f"Added device: {device.model}"))
