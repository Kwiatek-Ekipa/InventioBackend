from django.core.management import BaseCommand

from shared.enums import RoleEnum
from inventio_auth.models import Account, Role
from inventio_backend.settings import (SEED_TECHNICIAN1_EMAIL, SEED_TECHNICIAN1_PASSWORD,
                                       SEED_TECHNICIAN2_EMAIL, SEED_TECHNICIAN2_PASSWORD,)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dev",
            action="store_true"
        )


    def handle(self, *args, **options):
        if not Role.objects.filter(name=RoleEnum.TECHNICIAN.value).exists():
            print(self.style.ERROR("Technician role not found.\n"
                                   "Run 'python manage.py seedroles' first."))
            return

        if Account.objects.filter(email=SEED_TECHNICIAN1_EMAIL).exists():
            print(self.style.WARNING("Technician1 already exists."))
        else:
            try:
                Account.objects.create(
                    email=SEED_TECHNICIAN1_EMAIL,
                    password=SEED_TECHNICIAN1_PASSWORD,
                    name='Technician',
                    surname='Important',
                    role=RoleEnum.TECHNICIAN,
                    is_staff=True
                )
                print(self.style.SUCCESS("Technician1 created successfully."))
            except BaseException as e:
                raise e

        if options["dev"]:
            if Account.objects.filter(email=SEED_TECHNICIAN2_EMAIL).exists():
                print(self.style.WARNING("Technician2 already exists."))
            else:
                try:
                    Account.objects.create(
                        email=SEED_TECHNICIAN2_EMAIL,
                        password=SEED_TECHNICIAN2_PASSWORD,
                        name='Jarosław',
                        surname='Kaczyński',
                        role=RoleEnum.TECHNICIAN,
                        is_staff=True
                    )
                    print(self.style.SUCCESS("Technician2 created successfully."))
                except BaseException as e:
                    raise e
