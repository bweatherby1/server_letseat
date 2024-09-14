from rest_framework.decorators import api_view
from rest_framework.response import Response
from letseatapi.models import User
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def check_user(request):
    user_name = request.data.get('user_name')
    password = request.data.get('password')
   
    user = User.objects.filter(user_name=user_name).first()
   
    if user and check_password(password, user.password):
        data = {
            'uid': user.uid,
            'name': user.name,
            'user_name': user.user_name,
            'bio': user.bio,
            'profile_picture': user.profile_picture,
            'street_address': user.street_address,
            'city': user.city,
            'state': user.state,
            'zip_code': user.zip_code,
            'valid': True
        }
        return Response(data)
    else:
        return Response({'valid': False})







@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        name=request.data.get('name', ''),
        user_name=request.data.get('user_name', ''),
        bio=request.data.get('bio', ''),
        profile_picture=request.data.get('profile_picture', ''),
        street_address=request.data.get('street_address', ''),
        city=request.data.get('city', ''),
        state=request.data.get('state', ''),
        zip_code=request.data.get('zip_code', '')
    )
    user.set_password(request.data.get('password', ''))
    user.save()

    data = {
        'pk': user.pk,
        'uid': user.uid,
        'name': user.name,
        'user_name': user.user_name,
        'bio': user.bio,
        'profile_picture': user.profile_picture,
        'street_address': user.street_address,
        'city': user.city,
        'state': user.state,
        'zip_code': user.zip_code
    }
    return Response(data)
