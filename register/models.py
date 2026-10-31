from django.db import models
from django.contrib.auth.models import User,auth

# Create your models here.
class Pprofile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    cont_no=models.BigIntegerField(default=0)
    pfp=models.ImageField(upload_to="pfps",default="media\pfps\default\profile.jpg")
    update=models.DateTimeField(auto_now_add=True)
    add=models.TextField(blank=True)
    pin=models.IntegerField(default=0)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    aadhar=models.BigIntegerField()
    category=models.TextField(blank=True)
    
