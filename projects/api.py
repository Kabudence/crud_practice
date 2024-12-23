from rest_framework.response import Response

from .models import Project, Inventory, Item,SMSLog
from rest_framework import viewsets, permissions, status
from twilio.rest import Client
from django.conf import settings

from projects.serializers import ProjectSerializer,InventorySerializer,ItemSerializer,SMSLogSerializer
from rest_framework.views import APIView


# aca configurations el get y los permisos
# para ver quien pueden acceder a las consultas
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = InventorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        inventory_id = request.data.get('inventory_id')

        # Validar si el inventario existe
        if not Inventory.objects.filter(id=inventory_id).exists():
            return Response(
                {'error': f'El inventario con ID "{inventory_id}" no existe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el objeto Item
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            # Obtener el nombre del item recién creado
            item_name = response.data.get('name', 'el item')

            # Enviar SMS
            self.send_sms(f"Se ha registrado correctamente el item '{item_name}'.")

        return response

    def send_sms(self, message):
        try:
            # Inicializar cliente de Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            # Enviar SMS al número fijo
            twilio_message = client.messages.create(
                to="+51957244746",
                from_=settings.TWILIO_PHONE_NUMBER,
                body=message
            )

            # Guardar el log del SMS en caso de éxito (opcional)
            SMSLog.objects.create(
                to="+51957244746",
                message=message,
                sid=twilio_message.sid
            )

        except Exception as e:
            # Manejar errores de Twilio
            print(f"Error al enviar SMS: {str(e)}")


class SendSMSAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(f"SID: {settings.TWILIO_ACCOUNT_SID}, TOKEN: {settings.TWILIO_AUTH_TOKEN}")

        # Leer los datos del request
        to = request.data.get('to')
        message = request.data.get('message')

        if not to or not message:
            return Response(
                {"error": "Debe proporcionar 'to' (número de teléfono) y 'message'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Inicializar cliente de Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            # Enviar el SMS
            twilio_message = client.messages.create(
                to=to,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=message
            )

            return Response(
                {"message": "Mensaje enviado exitosamente.", "sid": twilio_message.sid},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
