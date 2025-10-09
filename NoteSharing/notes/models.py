from django.db import models
from users.models import Profile
# Create your models here.

class NoteTag(models.Model):
    title = models.CharField(max_length=30)

class Note(models.Model):
    title = models.CharField(max_length=30,blank=False)
    content = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='notePics/', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    editedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    tags = models.ManyToManyField(NoteTag,blank=True,null=True)



