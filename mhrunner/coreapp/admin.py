from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Server, Workstation
from .tasks import update_servers, update_workstations


class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update_servers/', self.admin_view(self.update_servers_view), name='update-servers'),
            path('update_workstations/', self.admin_view(self.update_workstations_view), name='update-workstations'),
        ]
        return custom_urls + urls

    def update_servers_view(self, request):
        update_servers.delay()
        messages.success(request, "Servers update initiated.")
        return HttpResponseRedirect('../')

    def update_workstations_view(self, request):
        update_workstations.delay()
        messages.success(request, "Workstations update initiated.")
        return HttpResponseRedirect("../")

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_buttons'] = format_html(
            '<a class="button" href="{}">Update Servers</a> '
            '<a class="button" href="{}">Update Workstations</a>',
            reverse('admin:update-servers'),
            reverse('admin:update-workstations')
        )
        return super().index(request, extra_context=extra_context)

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Server)
admin_site.register(Workstation)
