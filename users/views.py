from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from .models import User
from .serializers import UserSerializer
from .authentication import generate_access_token, JWTAuthentication

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
    
    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data={
        'jwt':token
    }
    return response 

# Logout
@api_view(['POST'])
def logout(_):
    response=Response()
    response.delete_cookie('jwt')
    response.data={
        'message': 'Success! jwt cookie deleted'
    }
    return response

# Authenticate via jwt cookie
class AuthenticatedUser(APIView):
    # Custom Middleware imported from authentication.py
    authentication_classes=[JWTAuthentication]
    
    # Prebuilt Middleware to check if it is authenticated before moving forward
    permission_classes=[IsAuthenticated] 

    def get(self, request):
        serializer=UserSerializer(request.user)
        return Response({
            'data':serializer.data
        })

# Users
@api_view(['GET'])
def users(request):
    serializer=UserSerializer( User.objects.all(),many=True)
    return Response(serializer.data)
