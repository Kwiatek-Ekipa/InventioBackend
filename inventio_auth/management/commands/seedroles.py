from django.core.management import BaseCommand

from shared.enums import RoleEnum
from inventio_auth.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_roles = Role.objects.filter(name__in=[role.value for role in RoleEnum])
        missing_roles = [role.value for role in RoleEnum if not db_roles.filter(name=role.value).exists()]

        if len(missing_roles) == 0:
            print('All roles have already been added.')

        for role in missing_roles:
            Role.objects.create(name=role)
            print(f'Added role: {role}.')


