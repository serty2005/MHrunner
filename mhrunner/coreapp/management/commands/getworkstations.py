from django.core.management.base import BaseCommand
from coreapp.getWorkstations import main as get_workstations_main

class Command(BaseCommand):
    help = 'Fetches data from workstations and populates the workstations model'

    def handle(self, *args, **kwargs):
        get_workstations_main()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and populated workstations data'))
