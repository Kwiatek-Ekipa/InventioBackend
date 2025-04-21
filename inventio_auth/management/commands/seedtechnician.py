from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError

from inventio_backend.settings import SEED_TECHNICIAN_EMAIL, SEED_TECHNICIAN_PASSWORD
from inventio_auth.enums import RoleEnum
from inventio_auth.models import Account, Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = get_user_model()

        if Account.objects.filter(role__name=RoleEnum.TECHNICIAN.value).exists():
            raise CommandError("Technician already exists.")
        try:
            user.objects.create(
                email=SEED_TECHNICIAN_EMAIL,
                password=SEED_TECHNICIAN_PASSWORD,
                name='System',
                surname='Technician',
                role=RoleEnum.TECHNICIAN,
                is_staff=True
            )

            print("Technician created successfully.")
        except Role.DoesNotExist:
            raise CommandError("Technician role not found.\n"
                               "Run 'python manage.py seedroles' first.")
