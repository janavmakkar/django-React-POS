from django.urls import path
from .views import register,login, AuthenticatedUser, logout, PermissionAPIView, RoleViewset, UserGenericAPIView

urlpatterns = [
    # path('users/', users),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('user/', AuthenticatedUser.as_view()),
    path('permissions/', PermissionAPIView.as_view()),
    
    path('roles/', RoleViewset.as_view({
        'get':'list',
        'post':'create'
    })),
    path('roles/<str:pk>', RoleViewset.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),

    path('users/',UserGenericAPIView.as_view()),
    path('users/<str:pk>',UserGenericAPIView.as_view())

]