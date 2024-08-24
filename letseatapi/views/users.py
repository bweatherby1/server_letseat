from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from letseatapi.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')
        
class UserViews(ViewSet):
    def retrieve(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
      
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.create(
            name=request.data["name"],
            uid=request.data["uid"]
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.name = request.data["name"]
        user.uid = request.data["uid"]
        user.save()

    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
