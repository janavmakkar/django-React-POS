from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated 
from users.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from admin.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage


# Create your views here.
class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, 
                         mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class=CustomPagination
    
    def get(self,request,pk=None):
        if pk:
            return Response({
                'data':self.retrieve(request,pk).data
            })
        return self.list(request)
    
    def post(self,request):
        return Response({
            'data':self.create(request).data
        })

    def put(self,request,pk=None):         
       return Response({
            'data':self.partial_update(request,pk).data
        })
    
    def delete(self,request,pk=None):
        return self.destroy(request,pk)

class FileUploadView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 
    # Parser Class to parse images
    parser_classes=(MultiPartParser)
    
    def post(self,request):
        file=request.FILES['image']
        file_name=default_storage.save(file_name,file)
        url=default_storage.url(file_name)
        return Response({
            'url':url
        })
    

