from rest_framework.test import APIClient, APITestCase
from letseatapi.models import User
from django.contrib.auth.hashers import make_password

class AuthViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            password=make_password('testpassword'),
            user_name='testuser',
            bio='Test bio',
            profile_picture='https://example.com/test.jpg',
            street_address='123 Test St',
            city='Test City',
            state='TS',
            zip_code='12345'
        )

    def test_check_user_valid(self):
        data = {
            'user_name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/checkuser', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['valid'])

    def test_check_user_invalid(self):
        data = {
            'user_name': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/checkuser', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'valid': False})

    def test_register_user(self):
        data = {
            'name': 'New User',
            'password': 'newpassword',
            'user_name': 'newuser',
            'bio': 'New user bio',
            'profile_picture': 'https://example.com/new.jpg',
            'street_address': '456 New St',
            'city': 'New City',
            'state': 'NS',
            'zip_code': '67890'
        }
        response = self.client.post('/register', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertIn('uid', response.data)
        self.assertEqual(response.data['name'], 'New User')
        self.assertEqual(response.data['user_name'], 'newuser')

        new_user = User.objects.get(user_name='newuser')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.name, 'New User')
        self.assertEqual(new_user.user_name, 'newuser')
        self.assertEqual(new_user.bio, 'New user bio')
        self.assertEqual(new_user.profile_picture, 'https://example.com/new.jpg')
        self.assertEqual(new_user.street_address, '456 New St')
        self.assertEqual(new_user.city, 'New City')
        self.assertEqual(new_user.state, 'NS')
        self.assertEqual(new_user.zip_code, '67890')
