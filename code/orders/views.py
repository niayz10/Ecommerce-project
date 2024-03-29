from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from orders import permissions

from . import models, serializers, services
from utils import mixins


class OrderItemViewSet(ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()


class OrderViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateOrderSerializer,
    }
    order_services: services.OrderServicesInterface = services.OrderServicesV1()
    queryset = order_services.get_orders()
    serializer_class = serializers.OrderSerializer
    permission_classes = permissions.IsCustomer,
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.order_services.create_order(data=serializer.validated_data)
        data = serializers.OrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)