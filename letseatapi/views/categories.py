from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from letseatapi.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CategoryView(ViewSet):
    def retrieve(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
      
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        category = Category.objects.create(
            name=request.data["name"]
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data)
      
    def update(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.name = request.data["name"]
        category.save
        
    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
