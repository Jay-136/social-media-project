from rest_framework import serializers,validators
from django.contrib.auth.models  import User
from .models import *


class RegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta :
        model = User
        fields = ["first_name","last_name","email","username","password","confirm_password"]
        extra_kwargs = {"password" : {"write_only" : True} }

    def save(self):
        Person = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email = self.validated_data['email']
        )
        Person.set_password(self.validated_data['password'])
        Person.save()
        return Person

    def validate(self,value):
        if value['password'] != value['confirm_password'] :
            return serializers.ValidationError("Password and Confirm Password are not same")
        if User.objects.filter(email=value['email']).exists():
            return serializers.ValidationError("This email is already exists")
        return value
    

class Postserializers(serializers.ModelSerializer):

    class Meta :
        model=Post
        fields="__all__"
        
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
        
        
class Commentserializers(serializers.ModelSerializer):
    
    class Meta :
        model = Comment
        fields = ['user','post','comment']
        