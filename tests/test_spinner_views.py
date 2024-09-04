from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from letseatapi.models import Spinner, User
from letseatapi.views.spinners import SpinnerSerializer

class SpinnerViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(uid='user1')
        self.user2 = User.objects.create(uid='user2')
        self.spinner = Spinner.objects.create(primary_user=self.user1, secondary_user=self.user2)




    def test_retrieve_spinner(self):
        response = self.client.get(f'/spinners/{self.spinner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.spinner.id)

    def test_list_spinners(self):
        response = self.client.get('/spinners')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_spinner(self):
        data = {'primary_user': self.user1.id, 'secondary_user': self.user2.id}
        response = self.client.post('/spinners', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_spinner(self):
        data = {'primary_user': self.user2.id, 'secondary_user': self.user1.id}
        response = self.client.put(f'/spinners/{self.spinner.id}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_spinner(self):
        response = self.client.delete(f'/spinners/{self.spinner.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
