from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BaseAuthentication
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework import status,viewsets
from .models import *


# Create your views here.


@api_view(["POST"])
def Register(request):
    if request.method == "POST" :
        serializer=RegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=201)
        
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