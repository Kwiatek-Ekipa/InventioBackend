from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dev",
            action="store_true"
        )

    def handle(self, *args, **options):
        call_command("seedroles")

        if options["dev"]:
            call_command("seedworkers")
            call_command("seedtechnicians", "--dev")
        else:
            call_command("seedtechnicians")