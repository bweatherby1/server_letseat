from rest_framework.decorators import api_view
from rest_framework.response import Response
from letseatapi.models import User
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def check_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = User.objects.filter(name=username).first()
    
    if user and check_password(password, user.password):
        data = {
            'id': user.id,
            'uid': user.uid,
            'name': user.name
        }
        return Response(data)
    else:
        return Response({'valid': False}, status=400)

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
