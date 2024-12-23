from rest_framework import serializers
from .models import Project, Item,Inventory,SMSLog


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'technology', 'created_at')
        read_only_fields = ('id', 'created_at',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'inventory_id','created_at')
        read_only_fields = ('id', 'created_at',)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'description', 'created_at')
        read_only_fields = ('id', 'created_at',)


class SMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLog
        fields = '__all__'  # Incluir todos los campos
