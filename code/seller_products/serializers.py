from rest_framework import serializers
from . import models
from products import serializers as product_serializers


class CreateSellerProductSerializer(serializers.ModelSerializer):
    # второй способ исключить, что другой продавец  создаст продукт на другого продавца
    # Таким образом это помогает создовать и подвязывать товар на пользователя, который его создал
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SellerProduct
        fields = ('seller', 'product', 'amount', 'amount_currency', 'is_active')

class UpdateSellerProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SellerProduct
        fields = ('amount', 'amount_currency', 'is_active')

class SellerProductSerializer(serializers.ModelSerializer):
    product = product_serializers.ProductSerializer()

    class Meta:
        model = models.SellerProduct
        fields = '__all__'