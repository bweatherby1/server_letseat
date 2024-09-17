from rest_framework import viewsets
from rest_framework.decorators import action
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
            # Find all selections for this restaurant by the specific user
            selected_restaurants = SelectedRestaurant.objects.filter(
                restaurant__id=restaurant_id, user__uid=user_uid
            )
            
            if selected_restaurants.exists():
                selected_restaurants.delete()
                return Response({'message': 'Restaurant removed from selection'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Selection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def by_user(self, request):
        user_uid = request.query_params.get('user_uid')
        if not user_uid:
            return Response({'error': 'User UID is required'}, status=status.HTTP_400_BAD_REQUEST)

        selected_restaurants = SelectedRestaurant.objects.filter(user__uid=user_uid)
        serializer = SelectedRestaurantSerializer(selected_restaurants, many=True)
        return Response(serializer.data)
