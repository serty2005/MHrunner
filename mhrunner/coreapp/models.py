from django.db import models

class Server(models.Model):
    UUID = models.CharField(max_length=255, primary_key=True)
    Teamviewer = models.CharField(max_length=255, null=True, blank=True)
    UniqueID = models.CharField(max_length=255, null=True, blank=True)
    IP = models.CharField(max_length=255, null=True, blank=True)
    CabinetLink = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    AnyDesk = models.CharField(max_length=255, null=True, blank=True)
    DeviceName = models.CharField(max_length=255, null=True, blank=True)
    ownerUUID = models.CharField(max_length=255, null=True, blank=True)
    ownerTitle = models.CharField(max_length=255, null=True, blank=True)
    cleared_ip = models.CharField(max_length=255, null=True, blank=True)

class Workstation(models.Model):
    UUID = models.CharField(max_length=255, primary_key=True)
    GK = models.CharField(max_length=255, null=True, blank=True)
    Teamviewer = models.CharField(max_length=255, null=True, blank=True)
    AnyDesk = models.CharField(max_length=255, null=True, blank=True)
    DeviceName = models.CharField(max_length=255, null=True, blank=True)
    lastModifiedDate = models.DateTimeField(null=True, blank=True)
    ownerTitle = models.CharField(max_length=255, null=True, blank=True)
    ownerUUID = models.CharField(max_length=255, null=True, blank=True)
    
