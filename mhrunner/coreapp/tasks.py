# coreapp/tasks.py
from celery import shared_task
from coreapp.getServers import main as get_servers_main
from coreapp.getWorkstations import main as get_workstations_main

@shared_task
def update_servers():
    get_servers_main()

@shared_task
def update_workstations():
    get_workstations_main()
