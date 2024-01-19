import logging
import random

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import serializers
from utils import mixins
from . import permissions
from . import services
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)

class ProductImageViewset(ModelViewSet):
    product_image_services: services.ProductImageServicesInterface = services.ProductImageServicesV1()
    queryset = product_image_services.get_product_images()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = permissions.IsAdminOrReadOnly,


class ProductViewset(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer,
    }
    serializer_class = serializers.ProductSerializer
    product_services: services.ProductServicesInterface = services.ProductServicesV1()
    queryset = product_services.get_products()
    permission_classes = permissions.IsAdminOrReadOnly,

    # def list(self, request, *args, **kwargs):
    #     number = random.choice('0123456789')

    #     output = _('Your number is {}').format(number)
    #     logger.info(output)

    #     return Response({'output': output})

    def list(self, request, *args, **kwargs):
        
        return super().list(request, *args, **kwargs)
