from django.core.management import BaseCommand

from inventio_auth.models import Account, Role
from inventio_backend.settings import (SEED_WORKER1_EMAIL, SEED_WORKER1_PASSWORD,
                                       SEED_WORKER2_EMAIL, SEED_WORKER2_PASSWORD)
from shared import RoleEnum


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Role.objects.filter(name=RoleEnum.WORKER.value).exists():
            print(self.style.ERROR("Worker role not found.\n"
                                   "Run 'python manage.py seedroles' first."))
            return

        if Account.objects.filter(email=SEED_WORKER1_EMAIL).exists():
            print(self.style.WARNING("Worker1 already exists."))
        else:
            try:
                Account.objects.create(
                    email=SEED_WORKER1_EMAIL,
                    password=SEED_WORKER1_PASSWORD,
                    name='Janusz',
                    surname='Kowalski',
                    role=RoleEnum.WORKER,
                    is_staff=False
                )
                print(self.style.SUCCESS("Worker1 created successfully."))
            except BaseException as e:
                raise e

        if Account.objects.filter(email=SEED_WORKER2_EMAIL).exists():
            print(self.style.WARNING("Worker2 already exists."))
        else:
            try:
                Account.objects.create(
                    email=SEED_WORKER2_EMAIL,
                    password=SEED_WORKER2_PASSWORD,
                    name='Zbigniew',
                    surname='Stonoga',
                    role=RoleEnum.WORKER,
                    is_staff=False
                )
                print(self.style.SUCCESS("Worker2 created successfully."))
            except BaseException as e:
                raise e