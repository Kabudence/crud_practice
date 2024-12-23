from django.db import models


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    inventory_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SMSLog(models.Model):
    to = models.CharField(max_length=15)  # Número de teléfono destino
    message = models.TextField()          # Contenido del mensaje
    status = models.CharField(max_length=50, blank=True, null=True)  # Estado del mensaje (success, failed, etc.)
    sid = models.CharField(max_length=50, blank=True, null=True)  # Twilio SID
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de envío

    def __str__(self):
        return f"To: {self.to}, Status: {self.status}"