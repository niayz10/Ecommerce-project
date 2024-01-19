from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import serializers, models
from utils import mixins
from . import permissions

class SellerProductViewSet(mixins.ActionSerializerMixin, mixins.ActionPermissionMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateSellerProductSerializer,
        'update': serializers.UpdateSellerProductSerializer,
        'partial_update': serializers.UpdateSellerProductSerializer,
    }
    ACTION_PERMISSIONS = {
        'update': (permissions.IsSellerAndOwner(),),
        'partial_update': (permissions.IsSellerAndOwner(),),
        'destroy': (permissions.IsSellerAndOwner(),),
    }
    
    serializer_class = serializers.SellerProductSerializer
    queryset = models.SellerProduct.objects.select_related('seller', 'product')
    permission_classes = permissions.IsSellerOrReadOnly,


    # Для вытаскивания пользователя при post запросе, чтобы продукт мог создать только владелец 
    # и ему не могли назначить не его товар
    # 1 способ
    # def perform_create(self, serializer):
    #     serializer.save(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save()