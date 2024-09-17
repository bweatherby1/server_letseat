from django.http import HttpResponseServerError, JsonResponse
from json import loads
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
from letseatapi.models import Restaurant, Category, User, SelectedRestaurant, Spinner


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'street_address', 'city', 'state', 'zip_code', 'image_url', 'category', 'user')
        
class RestaurantViews(ViewSet):
    def retrieve(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def list(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
      category = Category.objects.get(pk=request.data["category"])
      user = User.objects.get(pk=request.data["user"])
      
      restaurant = Restaurant.objects.create(
            name=request.data["name"],
            street_address=request.data["street_address"],
            city=request.data["city"],
            state=request.data["state"],
            zip_code=request.data["zip_code"],
            image_url=request.data["image_url"],
            category=category,
            user=user
        )
      serializer = RestaurantSerializer(restaurant)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.name = request.data.get("name", restaurant.name)
        restaurant.street_address = request.data.get("street_address", restaurant.street_address)
        restaurant.city = request.data.get("city", restaurant.city)
        restaurant.state = request.data.get("state", restaurant.state)
        restaurant.zip_code = request.data.get("zip_code", restaurant.zip_code)
        category = Category.objects.get(pk=request.data.get("category", restaurant.category.id))
        restaurant.category = category
        user = User.objects.get(uid=request.data.get("user", restaurant.user.uid))
        restaurant.user = user
        restaurant.save()
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)


        
    def destroy(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def in_spinner(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.joined = not restaurant.joined
        restaurant.save()
        message = 'Restaurant added to spinner' if restaurant.joined else 'Restaurant removed from spinner'
        return Response({'message': message}, status=status.HTTP_201_CREATED)


    @action(methods=['get'], detail=False)
    def by_category(self, request):
        restaurants = Restaurant.objects.filter(category=request.query_params.get('category'))
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def by_zip_code(self, request):
        restaurants = Restaurant.objects.filter(zip_code=request.query_params.get('zip_code'))
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def by_city(self, request):
        restaurants = Restaurant.objects.filter(city=request.query_params.get('city'))
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def by_user(self, request):
        restaurants = Restaurant.objects.filter(user=request.query_params.get('user'))
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
