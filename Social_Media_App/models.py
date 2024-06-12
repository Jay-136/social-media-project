from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    mobile=PhoneNumberField(null=True, blank=True)




class Post(models.Model):
    title=models.CharField()
    image=models.ImageField(upload_to="Pictures",null=True)
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