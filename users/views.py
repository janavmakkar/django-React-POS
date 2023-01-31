from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def register(request):
    data=request.data
    
    # if User.objects.filter(email=data['email']).exists():
    #     raise exceptions.APIException('User with this email already exists')
    
    if data['password'] != data['confirm_password']:
        raise exceptions.APIException('Passwords do not match')
    
    serializer=UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def users(request):
    users=User.objects.all()
    return Response(users)
