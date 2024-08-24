from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from letseatapi.models import Spinner, User, Restaurant

class SpinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spinner
        fields = ('id', 'primary_user', 'secondary_user', 'restaurant')

class SpinnerViews(ViewSet):
    def retrieve(self, request, pk):
        spinner = Spinner.objects.get(pk=pk)
        serializer = SpinnerSerializer(spinner)
        return Response(serializer.data)

    def list(self, request):
        spinners = Spinner.objects.all()
        serializer = SpinnerSerializer(spinners, many=True)
        return Response(serializer.data)

    def create(self, request):
        primary_user = User.objects.get(pk=request.data["primary_user"])
        secondary_user = User.objects.get(pk=request.data["secondary_user"])
        restaurant = Restaurant.objects.get(pk=request.data["restaurant"])

        spinner = Spinner.objects.create(
            primary_user=primary_user,
            secondary_user=secondary_user,
            restaurant=restaurant
        )
        serializer = SpinnerSerializer(spinner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        spinner = Spinner.objects.get(pk=pk)
        spinner.primary_user = User.objects.get(pk=request.data["primary_user"])
        spinner.secondary_user = User.objects.get(pk=request.data["secondary_user"])
        spinner.restaurant = Restaurant.objects.get(pk=request.data["restaurant"])
        spinner.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        spinner = Spinner.objects.get(pk=pk)
        spinner.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
