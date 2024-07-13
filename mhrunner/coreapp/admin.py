from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Server, Workstation
from django.core.management import call_command


def run_get_servers_command(modeladmin, request, queryset):
    try:
        call_command('getservers')
        modeladmin.message_user(request, "Successfully fetched and populated Servers data", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, str(e), messages.ERROR)

run_get_servers_command.short_description = "Run get servers command"

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    actions = [run_get_servers_command]


def run_get_workstations_command(modeladmin, request, queryset):
    try:
        call_command('getworkstations')
        modeladmin.message_user(request, "Successfully fetched and populated Workstations data", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, str(e), messages.ERROR)

run_get_workstations_command.short_description = "Run get workstations command"

@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    actions = [run_get_workstations_command]

class MyAdminSite(admin.AdminSite):
    site_header = 'My Administration'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update_servers/', self.admin_view(self.update_servers), name='update_servers'),
            path('update_workstations/', self.admin_view(self.update_workstations), name='update_workstations'),
        ]
        return custom_urls + urls

    def update_servers(self, request):
        try:
            call_command('getservers')
            self.message_user(request, "Successfully fetched and populated Servers data", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, str(e), level=messages.ERROR)
        return HttpResponseRedirect('/admin/')

    def update_workstations(self, request):
        try:
            call_command('getworkstations')
            self.message_user(request, "Successfully fetched and populated Workstations data", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, str(e), level=messages.ERROR)
        return HttpResponseRedirect('/admin/')

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Server, ServerAdmin)
admin_site.register(Workstation, WorkstationAdmin)

# Применение пользовательского админ-сайта
urlpatterns = [
    path('admin/', admin_site.urls),
]


# admin.site.register(Server)
# admin.site.register(Workstation)


