from django.shortcuts import render
from .models import Server, Workstation


def connections_view(request):
    owners = []
    servers = Server.objects.all()
    workstations = Workstation.objects.all()

    # Группировка серверов и станций по владельцам
    owner_uuids = set([server.ownerUUID for server in servers if server.ownerUUID])
    owner_uuids.update([workstation.ownerUUID for workstation in workstations if workstation.ownerUUID])

    for owner_uuid in owner_uuids:
        owner = {'ownerTitle': '', 'servers': [], 'workstations': []}
        servers_for_owner = servers.filter(ownerUUID=owner_uuid)
        workstations_for_owner = workstations.filter(ownerUUID=owner_uuid)

        if servers_for_owner.exists():
            owner['ownerTitle'] = servers_for_owner.first().ownerTitle
            owner['servers'] = servers_for_owner

        if workstations_for_owner.exists():
            owner['ownerTitle'] = workstations_for_owner.first().ownerTitle
            owner['workstations'] = workstations_for_owner

        owners.append(owner)

    return render(request, 'coreapp/connections.html', {'owners': owners})
