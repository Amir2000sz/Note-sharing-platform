from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Display_name = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    family = models.CharField(max_length=200,blank=True,null=True)
    number = models.CharField(max_length=20,unique=True,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    email = models.EmailField(max_length=35,unique=True)
    ProfileImage = models.ImageField(upload_to='profilePics/',blank=True,null=True,default="user.png")
    createdDate = models.DateField(auto_now_add=True)
    lastSeen = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name +" "+self.family)

class UserTag(models.Model):
    title = models.CharField(max_length=30)
    profile = models.ManyToManyField(Profile)
