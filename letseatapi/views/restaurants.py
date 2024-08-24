from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from letseatapi.models import Restaurant, Category, User


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'street_address', 'city', 'state', 'zip_code', 'image_url', 'category', 'user')
        
class RestaurantViews(ViewSet):
    def retrieve(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)
      
    def list(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
      
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
      return Response(serializer.data)
      
    def update(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.name = request.data["name"]
        restaurant.street_address = request.data["street_address"]
        restaurant.city = request.data["city"]
        restaurant.state = request.data["state"]
        restaurant.zip_code = request.data["zip_code"]
        restaurant.image_url = request.data["image_url"]
        restaurant.category = request.data["category"]
        restaurant.user = request.data["user"]
        restaurant.save
        
    def destroy(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def in_spinner(self, request, pk):
        restaurant = self.get_object()
        restaurant.joined = not restaurant.joined
        restaurant.save()
        return Response({'message': 'Restaurant added to spinner'}, status=status.HTTP_201_CREATED)
    
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
