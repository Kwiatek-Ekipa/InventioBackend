from django.core.management import BaseCommand
from inventio_auth.management.commands import seedroles, seedtechnician


class Command(BaseCommand):
    def handle(self, *args, **options):
        seedroles.Command().handle(args, options)
        seedtechnician.Command().handle(args, options)