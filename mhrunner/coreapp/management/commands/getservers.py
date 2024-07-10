# coreapp/management/commands/getservers.py
from django.core.management.base import BaseCommand
from coreapp.getServers import main as get_servers_main

class Command(BaseCommand):
    help = 'Fetches data from servers and populates the Servers model'

    def handle(self, *args, **kwargs):
        get_servers_main()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and populated Servers data'))
