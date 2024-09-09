from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from letseatapi.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'uid', 'password', 'user_name', 'bio', 'profile_picture', 'street_address', 'city', 'state', 'zip_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            uid=validated_data['uid'],
            user_name=validated_data['user_name'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', ''),
            street_address=validated_data['street_address'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.name = request.data["name"]
        user.user_name = request.data["user_name"]
        user.bio = request.data.get("bio", user.bio)
        user.profile_picture = request.data.get("profile_picture", user.profile_picture)
        user.street_address = request.data["street_address"]
        user.city = request.data["city"]
        user.state = request.data["state"]
        user.zip_code = request.data["zip_code"]
        if 'password' in request.data:
            user.set_password(request.data["password"])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
