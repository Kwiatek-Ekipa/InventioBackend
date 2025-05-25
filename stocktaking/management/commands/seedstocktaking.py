import random
from datetime import datetime, timedelta
from random import randint
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from inventio_auth.models import Role, Account
from shared import RoleEnum
from stocktaking.models import Stocktaking
from hardware.models import Device

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            technician_role = Role.objects.get(name=RoleEnum.TECHNICIAN.value)
            worker_role = Role.objects.get(name=RoleEnum.WORKER.value)
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Technician or worker role does not exist. Please run `python manage.py seedroles` first!"
            ))
            return

        technicians = Account.objects.filter(role=technician_role)
        if not technicians.exists():
            self.stdout.write(self.style.ERROR(
                "No technician account found. Please run `python manage.py seedtechnicians --dev` first!"
            ))
            return

        workers = Account.objects.filter(role=worker_role)
        if not workers.exists():
            self.stdout.write(self.style.ERROR(
                "No worker account found. Please run `python manage.py seedworkers` or `python manage.py seedauth --dev` first!"
            ))
            return

        devices = Device.objects.all()
        if not devices.exists():
            self.stdout.write(self.style.ERROR(
                "No devices found. Please run `python manage.py seed_hardware` first!"
            ))
            return

        now = datetime.now()
        five_years_ago = now.replace(year=now.year - 5)

        for device in devices:
            if Stocktaking.objects.filter(device=device).exists():
                self.stdout.write(self.style.WARNING(f"Stocktaking for device '{device.model}' already exists. Skipping..."))
                continue

            random_release_date = make_aware(
                five_years_ago + timedelta(
                    seconds=random.randint(0, int((now - five_years_ago).total_seconds()))
                )
            )
            returned = random.choice([True, False])
            taken_back_by = random.choice(technicians) if returned else None
            stocktaking_data = {
                "release_date": random_release_date,
                "recipient": random.choice(workers),
                "device": device,
                "released_by": random.choice(technicians),
            }

            if returned:
                stocktaking_data["return_date"] = random_release_date + timedelta(days=random.randint(60, 180))
                # Technically, that date can be more than the current date, but just for testing purposes, I think it will be enough ¯\_(ツ)_/¯
                stocktaking_data["taken_back_by"] = taken_back_by

            Stocktaking.objects.create(**stocktaking_data)
            self.stdout.write(self.style.SUCCESS(f"Added stocktaking for device: {device.model}"))
