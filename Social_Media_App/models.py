from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Post(models.Model):
    title=models.CharField()
    image=models.ImageField()
    content=models.TextField()
    tag=models.CharField()
    posted_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    class Meta :
        unique_together=('user','post')
        
        
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.TextField(max_length=150)