from django.core.management import BaseCommand
from inventio_auth.management.commands import seedroles, seedtechnicians, seedworkers


class Command(BaseCommand):
    def handle(self, *args, **options):
        seedroles.Command().handle(args, options)
        seedtechnicians.Command().handle(args, options)
        seedworkers.Command().handle(args, options)