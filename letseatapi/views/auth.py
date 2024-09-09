from rest_framework.decorators import api_view
from rest_framework.response import Response
from letseatapi.models import User
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def check_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
   
    user = User.objects.filter(user_name=username).first()
   
    if user and check_password(password, user.password):
        data = {
            'id': user.id,
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
    else:
        return Response({'valid': False}, status=400)

@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        name=request.data['name'],
        uid=request.data['uid'],
        user_name=request.data['user_name'],
        bio=request.data.get('bio', ''),
        profile_picture=request.data.get('profile_picture', ''),
        street_address=request.data['street_address'],
        city=request.data['city'],
        state=request.data['state'],
        zip_code=request.data['zip_code']
    )
    user.set_password(request.data['password'])
    user.save()

    data = {
        'id': user.id,
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
