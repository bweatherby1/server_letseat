from rest_framework.decorators import api_view
from rest_framework.response import Response
from letseatapi.models import User
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def check_user(request):
    uid = request.data['uid']
    user = User.objects.filter(uid=uid).first()
    if user is not None and check_password(request.data['password'], user.password):
        data = {
            'id': user.id,
            'uid': user.uid,
            'name': user.name
        }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        name=request.data['name'],
        uid=request.data['uid']
    )
    user.set_password(request.data['password'])
    user.save()

    data = {
        'id': user.id,
        'uid': user.uid,
        'name': user.name
    }
    return Response(data)
