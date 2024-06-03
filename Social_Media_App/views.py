from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BaseAuthentication
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework import status,viewsets,filters,generics
from .models import *
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.


# @api_view(["POST"])
# def Register(request):
#     # if request.method == "POST" :
#         email=EmailMessage("welcome to Social Media App",f"Hey {request.data.get('first_name')}, Thank you for registration in Social Media App",
#         settings.EMAIL_HOST_USER,[request.data.get('email')])
#         serializer=RegistrationSerializers(data=request.data)
        
#         if serializer.is_valid(raise_exception=True):
#             email.send()
#             serializer.save()
#             return Response(serializer.data,status=201)
        
        
class Register(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=[AllowAny]
    serializer_class= RegistrationSerializers
    
    
class LogIn(generics.CreateAPIView):
    pass
    
        
        
        
@api_view(["POST"]) 
def Logout(request):
    if request.method == "POST":
        try :
            request.user.auth_token.delete()
            return Response({"message":"Successfully logout"},status=status.HTTP_200_OK)

        except :
            return Response({"message":"User already logout"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class uploadORupdate(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class= Postserializers
    search_fields = ['tag', 'title']
    filterset_fields = ['title', 'tag','content','user']
    
class Likeview(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class= Likeserializers
    filterset_fields = ['user','post']
    
class Commentview(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=Commentserializers
    filterset_fields = ['user','post','comment']
    
    
    
   
    
    