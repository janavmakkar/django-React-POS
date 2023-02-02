from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from .models import User
from .serializers import UserSerializer

# Register
@api_view(['POST'])
def register(request):
    data=request.data
    
    if data['password'] != data['confirm_password']:
        raise exceptions.APIException('Passwords do not match')
    
    serializer=UserSerializer(data= data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

# Login
@api_view(['POST'])
def login(request):
    email=request.data.get('email')
    password=request.data.get('password')
    user=User.objects.filter(email=email).first()
    if( user is None):
        raise exceptions.AuthenticationFailed('User not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Wrong Password!')
    return Response('Success')



# Users
@api_view(['GET'])
def users(request):
    serializer=UserSerializer( User.objects.all(),many=True)
    return Response(serializer.data)
