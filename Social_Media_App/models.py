from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from os.path import splitext
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    mobile=PhoneNumberField(null=True, blank=True)
    first_name = models.CharField(("first name"), max_length=150, blank=True,null=True)
    last_name = models.CharField(("last name"), max_length=150, blank=True,null=True)

def validated_file(value):
    extentions = splitext(value.name)[1]
    valid_extentions = [".pdf",".jpeg",".png"]
    if extentions.lower() not in valid_extentions :
        raise ValidationError("this file format is not supported")
    
    file_size = value.size
    if file_size>3*1024*1024: #3MB
        raise ValidationError("the file size is very big")

class Post(models.Model):
    title=models.CharField()
    image=models.FileField(upload_to="Pictures",null=True,blank=True,validators=[validated_file])
    content=models.TextField(null=True, blank=True)
    tag=models.CharField()
    posted_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_Like",related_query_name="user_Like",null=True, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_Like",related_query_name="post_Like")
    
    class Meta :
        unique_together=('user','post')
        
        
class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_Comment",related_query_name="user_Comment",null=True, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_Comment",related_query_name="post_Comment")
    comment=models.TextField(max_length=150)