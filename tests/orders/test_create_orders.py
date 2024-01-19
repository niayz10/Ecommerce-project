from datetime import timedelta
from django.utils import timezone
import pytest

from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import status


from orders import repositories
from products import models
import seller_products
from seller_products.choices import CurrencyChoices
from seller_products.models import SellerProduct
import helpers
from payments import models  as payments_models, choices as payment_choices


@pytest.mark.django_db
class CreateOrderReposTest:
    order_repos: repositories.OrderRepositoriesInterface = repositories.OrderRepositoriesV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')


    @pytest.mark.parametrize('user_id, seller_product_ides', (
            ('ab55f98d-8ef8-4e93-91a4-184013cb5afe', (1,)),
            ('ab55f98d-8ef8-4e93-91a4-184013cb5afe', (1, 2)),
    ))
    @pytest.mark.freeze_time('2020-01-01')
    def test_create_order(self, user_id, seller_product_ides):
        user = get_user_model().objects.get(pk=user_id)
        seller_products = SellerProduct.objects.filter(id__in=seller_product_ides)
        order_items = [{'seller_product': seller_product} for seller_product in seller_products]

        data = {
            'customer': user,
            'order_items': order_items,
        }
        order, bill = self.order_repos.create_order(data)

        assert order.order_items.count() == len(order_items)

        total = order.order_items.aggregate(total=Sum('amount'))['total']
        assert total == sum(i['seller_product'].amount for i in order_items)
       
        
        assert bill.amount == bill.total == total
        assert bill.status == payment_choices.BillStatusChoices.New
        assert bill.expires_at == timezone.now() + timedelta(minutes=30)
        
        

@pytest.mark.django_db
class OrderViewTest(object):

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    @pytest.mark.parametrize('case, user_id, status_code', (
            ('1', 'ab55f98d-8ef8-4e93-91a4-184013cb5afe', status.HTTP_201_CREATED), 
            ('2', 'ab55f98d-8ef8-4e93-91a4-184013cb5afe', status.HTTP_201_CREATED), 
            ('3', 'ab55f98d-8ef8-4e93-91a4-184013cb5afe', status.HTTP_400_BAD_REQUEST), 
            ('4', 'ab55f98d-8ef8-4e93-91a4-184013cb5afe', status.HTTP_400_BAD_REQUEST), 
            ('5', 'ab55f98d-8ef8-4e93-91a4-184013cb5afe', status.HTTP_400_BAD_REQUEST),
            ('1', '5b4ef251-ba01-4a2f-9bcb-bebbcb9daedd', status.HTTP_403_FORBIDDEN), 
            ))
    def test_create_order(self, case, user_id, status_code, api_client):
        user = get_user_model().objects.get(pk=user_id)
        data = helpers.load_json_data(f'orders/create_order/{case}')
        response = api_client.post(
            '/api/v1/orders/',
            format='json',
            data=data,
            HTTP_AUTHORIZATION=helpers.access_token(user),
        )
       
        assert response.status_code == status_code