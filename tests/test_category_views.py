from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from letseatapi.models import Category

class CategoryViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category_data = {"name": "Test Category"}
        self.category = Category.objects.create(name="Existing Category")

    def test_list_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_category(self):
        response = self.client.get(reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_create_category(self):
        response = self.client.post(reverse('category-list'), self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        response = self.client.put(
            reverse('category-detail', args=[self.category.id]),
            {"name": "Updated Category"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")

    def test_delete_category(self):
        response = self.client.delete(reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
