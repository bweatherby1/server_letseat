from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from letseatapi.models import User

class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "name": "Test User",
            "uid": "testuid",
            "password": "testpass",
            "user_name": "testuser",
            "bio": "Test bio",
            "profile_picture": "https://example.com/test.jpg",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        }

    def test_retrieve_user(self):
        user = User.objects.create(
            name="Test User",
            uid="test123",
            user_name="testuser123",
            bio="Test bio",
            profile_picture="https://example.com/test123.jpg",
            street_address="456 Test Ave",
            city="Test Town",
            state="TT",
            zip_code="67890"
        )
        response = self.client.get(reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test User")
        self.assertEqual(response.data['user_name'], "testuser123")
        self.assertEqual(response.data['bio'], "Test bio")
        self.assertEqual(response.data['profile_picture'], "https://example.com/test123.jpg")
        self.assertEqual(response.data['street_address'], "456 Test Ave")
        self.assertEqual(response.data['city'], "Test Town")
        self.assertEqual(response.data['state'], "TT")
        self.assertEqual(response.data['zip_code'], "67890")

    def test_list_users(self):
        User.objects.create(name="User 1", uid="uid1", user_name="user1")
        User.objects.create(name="User 2", uid="uid2", user_name="user2")
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(name="Test User").exists())
        created_user = User.objects.get(name="Test User")
        self.assertEqual(created_user.user_name, "testuser")
        self.assertEqual(created_user.bio, "Test bio")
        self.assertEqual(created_user.profile_picture, "https://example.com/test.jpg")
        self.assertEqual(created_user.street_address, "123 Test St")
        self.assertEqual(created_user.city, "Test City")
        self.assertEqual(created_user.state, "TS")
        self.assertEqual(created_user.zip_code, "12345")

    def test_update_user(self):
        user = User.objects.create(name="Old Name", uid="olduid", user_name="olduser")
        update_data = {
            "name": "New Name",
            "password": "newpass",
            "user_name": "newuser",
            "bio": "Updated bio",
            "profile_picture": "https://example.com/updated.jpg",
            "street_address": "789 New St",
            "city": "New City",
            "state": "NS",
            "zip_code": "54321"
        }
        response = self.client.put(reverse('user-detail', args=[user.id]), data=update_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.name, "New Name")
        self.assertEqual(user.user_name, "newuser")
        self.assertEqual(user.bio, "Updated bio")
        self.assertEqual(user.profile_picture, "https://example.com/updated.jpg")
        self.assertEqual(user.street_address, "789 New St")
        self.assertEqual(user.city, "New City")
        self.assertEqual(user.state, "NS")
        self.assertEqual(user.zip_code, "54321")

    def test_delete_user(self):
        user = User.objects.create(name="To Delete", uid="deleteuid", user_name="deleteuser")
        response = self.client.delete(reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())
