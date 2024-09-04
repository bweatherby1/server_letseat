from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from letseatapi.models import Restaurant, Category, User

class RestaurantViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create()
        
        self.category = Category.objects.create(name='Test Category')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            street_address='123 Test St',
            city='Test City',
            state='TS',
            zip_code='12345',
            image_url='http://test.com/image.jpg',
            category=self.category,
            user=self.user
        )

    def test_retrieve_restaurant(self):
        response = self.client.get(f'/restaurants/{self.restaurant.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Restaurant')

    def test_list_restaurants(self):
        response = self.client.get('/restaurants')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_restaurant(self):
        new_restaurant_data = {
            'name': 'New Restaurant',
            'street_address': '456 New St',
            'city': 'New City',
            'state': 'NS',
            'zip_code': '67890',
            'image_url': 'http://new.com/image.jpg',
            'category': self.category.id,
            'user': self.user.id
        }
        response = self.client.post('/restaurants', new_restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_update_restaurant(self):
        update_data = {'name': 'Updated Restaurant'}
        response = self.client.put(f'/restaurants/{self.restaurant.id}', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')

    def test_delete_restaurant(self):
        response = self.client.delete(f'/restaurants/{self.restaurant.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0)

    def test_in_spinner(self):
        response = self.client.post(f'/restaurants/{self.restaurant.id}/in_spinner')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.restaurant.refresh_from_db()
        self.assertTrue(self.restaurant.joined)

    def test_by_category(self):
        response = self.client.get(f'/restaurants/by_category?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_zip_code(self):
        response = self.client.get('/restaurants/by_zip_code?zip_code=12345')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_city(self):
        response = self.client.get('/restaurants/by_city?city=Test City')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_user(self):
        response = self.client.get(f'/restaurants/by_user?user={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
