from django.contrib import admin
from .models import Server, Workstation
from django.core.management import call_command

# admin.site.register(Server)
# admin.site.register(Workstation)

def run_get_servers_command(modeladmin, request, queryset):
    call_command('getservers')

run_get_servers_command.short_description = "Run get servers command"

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    actions = [run_get_servers_command]


def run_get_workstations_command(modeladmin, request, queryset):
    call_command('getworkstations')

run_get_workstations_command.short_description = "Run get workstations command"

@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    actions = [run_get_workstations_command]
