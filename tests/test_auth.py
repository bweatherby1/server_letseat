from rest_framework.test import APIClient, APITestCase
from letseatapi.models import User
from django.contrib.auth.hashers import make_password

class AuthViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            uid='testuid123',
            password=make_password('testpassword')
        )

    def test_check_user_valid(self):
        data = {
            'uid': 'testuid123',
            'password': 'testpassword'
        }
        response = self.client.post('/checkuser', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['uid'], self.user.uid)
        self.assertEqual(response.data['name'], self.user.name)

    def test_check_user_invalid(self):
        data = {
            'uid': 'testuid123',
            'password': 'wrongpassword'
        }
        response = self.client.post('/checkuser', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'valid': False})

    def test_register_user(self):
        data = {
            'name': 'New User',
            'uid': 'newuid456',
            'password': 'newpassword'
        }
        response = self.client.post('/register', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data['uid'], 'newuid456')
        self.assertEqual(response.data['name'], 'New User')

        new_user = User.objects.get(uid='newuid456')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.name, 'New User')
