from django.contrib.auth import get_user_model
import pytest
from rest_framework import status
import helpers


@pytest.mark.django_db
class BillViewTest(object):


    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json', 'orders.json', 'bills.json')


    @pytest.mark.parametrize('bill_id', (
            'ab55f98d-8ef8-4e93-91a4-184013cb5afe',
    ))
    def test_pay_bill(self, bill_id, api_client):
        response = api_client.post(f'/api/v1/bills/{bill_id}/pay/')


        assert response.status_code == status.HTTP_204_NO_CONTENT