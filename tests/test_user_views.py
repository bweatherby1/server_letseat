from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from letseatapi.models import User

class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {"name": "Test User", "uid": "testuid", "password": "testpass"}

    def test_retrieve_user(self):
        user = User.objects.create(name="Test User", uid="test123")
        response = self.client.get(reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test User")

    def test_list_users(self):
        User.objects.create(name="User 1", uid="uid1")
        User.objects.create(name="User 2", uid="uid2")
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(name="Test User").exists())

    def test_update_user(self):
        user = User.objects.create(name="Old Name", uid="olduid")
        update_data = {"name": "New Name", "password": "newpass"}
        response = self.client.put(reverse('user-detail', args=[user.id]), data=update_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        self.assertEqual(user.name, "New Name")

    def test_delete_user(self):
        user = User.objects.create(name="To Delete", uid="deleteuid")
        response = self.client.delete(reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())
