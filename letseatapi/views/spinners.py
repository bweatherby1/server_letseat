from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from letseatapi.models import Spinner, User

class SpinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spinner
        fields = ( 'id', 'uid', 'primary_user', 'secondary_user',)

class SpinnerViews(ViewSet):
    def retrieve(self, request, uid):
        spinner = Spinner.objects.get(uid=uid)
        serializer = SpinnerSerializer(spinner)
        return Response(serializer.data)

    def list(self, request):
        spinners = Spinner.objects.all()
        serializer = SpinnerSerializer(spinners, many=True)
        return Response(serializer.data)

    def create(self, request):
        primary_user = User.objects.get(uid=request.data["primary_user"])
        secondary_user = User.objects.get(uid=request.data["secondary_user"])

        spinner = Spinner.objects.create(
            primary_user=primary_user,
            secondary_user=secondary_user
        )
        serializer = SpinnerSerializer(spinner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, uid):
        spinner = Spinner.objects.get(uid=uid)
        spinner.primary_user = User.objects.get(uid=request.data["primary_user"])
        spinner.secondary_user = User.objects.get(uid=request.data["secondary_user"])
        spinner.save()
        serializer = SpinnerSerializer(spinner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, uid):
        spinner = Spinner.objects.get(uid=uid)
        spinner.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
