from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--production",
            action="store_true"
        )

    def handle(self, *args, **options):
        call_command("seedroles")

        if options["production"]:
            print(self.style.SUCCESS("OUTER ARGUMENT WORKED!!!"))
            call_command("seedtechnicians", "--production")

        else:
            call_command("seedtechnicians")
            call_command("seedworkers")
