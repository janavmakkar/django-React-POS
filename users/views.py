from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from .authentication import generate_access_token, JWTAuthentication
from rest_framework import exceptions, viewsets, status, generics, mixins
from .models import User,Permission,Role
from .serializers import UserSerializer,PermissionSerializer,RoleSerializer
from admin.pagination import CustomPagination

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

# Show all permissions
class PermissionAPIView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 
    def get(self, request):
        serializer=PermissionSerializer(Permission.objects.all(),many=True)
        return Response({
            'data':serializer.data
        })

# Show all Roles
class RoleViewset(viewsets.ViewSet):
    # Viewsets does not have 'get' method, like APIView coz it is used 
    # to get both single item and list of items
    # To deal with that confusion Viewsets give many predfined functions
    # like - list, retrieve, create, update, destroy

    # GET
    def list(self,request):
        serializer=RoleSerializer(Role.objects.all(),many=True)
        return Response({
            'data':serializer.data
        })
    
    # POST
    def create(self,request):
        serializer=RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data':serializer.data
        },status=status.HTTP_201_CREATED)

    # GET
    def retrieve(self,request, pk=None):
        role=Role.objects.get(id=pk)
        serializer=RoleSerializer(role)
        return Response({
            'data':serializer.data
        })
    
    # PUT
    def update(self,request, pk=None):
        role=Role.objects.get(id=pk)
        serializer=RoleSerializer(instance=role,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data':serializer.data
        },status=status.HTTP_202_ACCEPTED)
    
    # DELETE
    def destroy(self,request, pk=None):
        role=Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API's for Users
class UserGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, 
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                         mixins.CreateModelMixin, mixins.DestroyModelMixin):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 
    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class=CustomPagination
    
    def get(self,request,pk=None):
        if pk:
            return Response({
                'data':self.retrieve(request,pk).data
            })
        return self.list(request)
    
    def post(self,request):
        request.data.update({
            'password':"root",              # every new user created gets default password "root"
            'role':request.data['role_id']  # use "role_id" from request data to fill "role" column
        })
        return Response({
            'data':self.create(request).data
        })

    def put(self,request,pk=None):         
        if (request.data['role_id']):         # if new "role" is provided to be updated then get it from "role_id"
            request.data.update({
                'role':request.data['role_id']
            })

        return Response({
            'data':self.partial_update(request,pk).data
        })
    
    def delete(self,request,pk=None):
        return self.destroy(request,pk)
        

