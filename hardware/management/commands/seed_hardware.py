from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Seed brands, categories, and devices for the hardware app."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding brands..."))
        call_command("seed_brands")

        self.stdout.write(self.style.NOTICE("Seeding categories..."))
        call_command("seed_categories")

        self.stdout.write(self.style.NOTICE("Seeding devices..."))
        call_command("seed_devices")

        self.stdout.write(self.style.SUCCESS("Hardware data seeding complete."))
