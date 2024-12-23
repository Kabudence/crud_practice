from rest_framework import routers
from django.urls import path
from .api import ProjectViewSet, InventoryViewSet, ItemViewSet, SendSMSAPIView

# Crear un router para los ViewSets
router = routers.DefaultRouter()
router.register('api/projects', ProjectViewSet, 'projects')
router.register('api/inventories', InventoryViewSet, 'inventories')
router.register('api/items', ItemViewSet, 'items')

# Registrar SendSMSAPIView como una URL separada
urlpatterns = router.urls + [
    path('api/send-sms/', SendSMSAPIView.as_view(), name='send-sms'),
]
