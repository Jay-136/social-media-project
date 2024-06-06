from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BaseAuthentication
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework import status, viewsets, generics, exceptions, authentication,filters
from .models import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PostNumberPagination,PostLimitOffsetPagination,PostCursorPagination

# Create your views here.

        
#====================================================================#   
#For New User Registration
#====================================================================#        
class Register(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    permission_classes=[AllowAny]
    serializer_class= RegistrationSerializers
    
    
#====================================================================#   
#For User Login
#====================================================================#    
class LogIn(generics.CreateAPIView):
    permission_classes=[AllowAny]
    def create(self, request, *args, **kwargs):
        # Get the username and password
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'username':username, 'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
#====================================================================#   
#For User Logout
#====================================================================#       
class Logout(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
        
     
        
class HasImageFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        
        hasimg = request.query_params.get('hasimg')
        if hasimg is not None:
            if hasimg.lower() == "true":
                queryset=queryset.exclude(image__isnull=True).exclude(image="")
                
            elif hasimg.lower()=="false":
                queryset=queryset.filter(image="")
                # print(queryset)
            else:
                raise serializers.ValidationError("Expected true or false")
        return queryset



#====================================================================#   
#For Post
#====================================================================#
class Postview(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('post_Comment', 'post_Like').all()
    filterset_fields=['title', 'content', 'tag', 'user'] 
    filter_backends=[HasImageFilter, DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'tag']
    pagination_class = PostLimitOffsetPagination
    
    def get_serializer_class(self):
        if self.action in ["listall", "retrieve","list"]:
            return Postserializers
        return PostCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user': user})
        return context
    
    @action(detail=False, methods=['get'])
    def listall(self, request):
        queryset = Post.objects.all().order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#====================================================================#   
#For Like
#====================================================================#
class Likeview(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = Likeserializers
    filterset_fields=['user', 'post']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user': user})
        return context
    
    
#====================================================================#   
#For Delete Like
#====================================================================#

@api_view(['DELETE',])
def remove_like(request):
    if request.method == 'DELETE':
        user_id = int(Token.objects.get(key=request.auth.key).user_id)
        if Like.objects.filter(user=user_id, post=request.data.get('post')).exists():
            Like.objects.filter(user=user_id, post=request.data.get('post')).delete()
            return Response({'message':'Unlike'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Already didn't like the post") 


#====================================================================#   
#For Comment
#====================================================================#
class Commentview(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = Commentserializers
    filterset_fields=['user', 'post', 'comment']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user': user})
        print(context)
        return context

    
    
    
   
    
    