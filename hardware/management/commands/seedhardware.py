from django.core.management import BaseCommand
from hardware.management.commands.seeddevices import Command as SeedDevicesCommand
from hardware.management.commands.seedcategories import Command as SeedCategoriesCommand
from hardware.management.commands.seedbrands import Command as SeedBrandsCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        print(self.style.NOTICE("Seeding brands..."))
        SeedBrandsCommand().handle(*args, **options)

        print(self.style.NOTICE("Seeding categories..."))
        SeedCategoriesCommand().handle(*args, **options)

        print(self.style.NOTICE("Seeding devices..."))
        SeedDevicesCommand().handle(*args, **options)

        print(self.style.SUCCESS("\nHardware data seeding complete."))
