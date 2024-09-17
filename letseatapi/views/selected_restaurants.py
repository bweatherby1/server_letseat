from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers, status
from letseatapi.models import Restaurant, SelectedRestaurant, User

class SelectedRestaurantSerializer(serializers.ModelSerializer):
    class Meta():
        model = SelectedRestaurant
        fields = ('id', 'restaurant', 'user')
        user_uid = serializers.UUIDField(source='user.uid', read_only=True)

class SelectedRestaurantViews(viewsets.ModelViewSet):
    queryset = SelectedRestaurant.objects.all()
    serializer_class = SelectedRestaurantSerializer

    def create(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant_id')
        user_uid = request.data.get('user_uid')  # Use user_uid instead of user_id

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            user = User.objects.get(uid=user_uid)  # Fetch user by uid
            selected_restaurant, created = SelectedRestaurant.objects.get_or_create(
                restaurant=restaurant, user=user
            )
            if created:
                return Response({'message': 'Restaurant added to selection'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Restaurant already selected'}, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': f'User with UID {user_uid} not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant_id')
        user_uid = request.data.get('user_uid')  # Use user_uid instead of user_id

        try:
            selected_restaurant = SelectedRestaurant.objects.get(
                restaurant__id=restaurant_id, user__uid=user_uid
            )
            selected_restaurant.delete()
            return Response({'message': 'Restaurant removed from selection'}, status=status.HTTP_200_OK)
        except SelectedRestaurant.DoesNotExist:
            return Response({'error': 'Selection not found'}, status=status.HTTP_404_NOT_FOUND)
