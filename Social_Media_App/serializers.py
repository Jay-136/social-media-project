from rest_framework import serializers,validators
from .models import *
from django.core.mail import EmailMessage
from django.conf import settings


class  CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        exclude = ['password','is_staff', 'is_active', 'user_permissions', 'groups', 'is_superuser', 'last_login']


class RegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only = True)

    class Meta :
        model = CustomUser
        fields = ["first_name","last_name","email","username","password","confirm_password"]
        extra_kwargs = {"password" : {"write_only" : True} }

    def save(self):
        Person = CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email = self.validated_data['email']
        )
        email = EmailMessage("Welcome to Social Media App",f"Hi {self.validated_data['first_name']}, thank you for registering in Social Media App.",settings.EMAIL_HOST_USER, [self.validated_data['email']])
        email.send()
        Person.set_password(self.validated_data['password'])
        Person.save()
        return Person

    def validate(self,value):
        if value['password'] != value['confirm_password'] :
            return serializers.ValidationError("Password and Confirm Password are not same")
        if CustomUser.objects.filter(email=value['email']).exists():
            return serializers.ValidationError("This email is already exists")
        return value
    
#====================================================================#   
#For Post Listing
#====================================================================#
class Postserializers(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    image_url=serializers.CharField(source='image')
    class Meta :
        model=Post
        fields=["title","image_url","content","tag","user","comment_count","like_count"]
        
    def get_comment_count(self, obj):
        return obj.post_Comment.count()
    
    def get_like_count(self, obj):
        return obj.post_Like.count()    

#====================================================================#   
#For Post Creating
#====================================================================#   
class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'tag', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        # print(validated_data)
        # print(self.context)
        return super().create(validated_data)

        
class Likeserializers(serializers.ModelSerializer):
    
    class Meta:
        model=Like
        fields=['user','post']
        validators =[
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("user","post"),
                message=("Already liked once")
            )
        ]
        
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)
        
        
class Commentserializers(serializers.ModelSerializer):
    
    class Meta :
        model = Comment
        fields = ['user','post','comment']
        
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        print(validated_data)
        print(self.context)
        return super().create(validated_data)
        