from django.core.management import BaseCommand, CommandError

from inventio_backend.settings import SEED_TECHNICIAN_EMAIL, SEED_TECHNICIAN_PASSWORD
from inventio_auth.enums import RoleEnum
from inventio_auth.models import Account, Role

class Command(BaseCommand):
    def handle(self, *args, **options):

        if Account.objects.filter(role__name=RoleEnum.TECHNICIAN.value).exists():
            raise CommandError("Technician already exists.")

        try:
            technician_role = Role.objects.get(name=RoleEnum.TECHNICIAN.value)

            technician = Account.objects.create(
                email=SEED_TECHNICIAN_EMAIL,
                name='Generated',
                surname='Technician',
                role=technician_role
            )
            technician.set_password(SEED_TECHNICIAN_PASSWORD)
            technician.save()

            print("Technician created successfully.")
        except Role.DoesNotExist:
            raise CommandError("Technician role not found.\n"
                               "Run 'python manage.py seedroles' first.")