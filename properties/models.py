from django.db import models
from root.models import Agent

# Create your models here.

class property_type(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
    
class Status(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title



class Property(models.Model):
    image1=models.ImageField(default='properties/default.jpg',upload_to='properties/')
    image2=models.ImageField(default='properties/default.jpg',upload_to='properties/')
    image3=models.ImageField(default='properties/default.jpg',upload_to='properties/')
    title=models.CharField()
    description=models.TextField()
    agent=models.ForeignKey(Agent,on_delete=models.DO_NOTHING)
    video=models.TextField()
    floor=models.ImageField(default='properties/default.jpg',upload_to='properties/')
    map=models.TextField()
    location=models.CharField()
    type=models.ForeignKey(property_type,on_delete=models.DO_NOTHING)
    beds=models.IntegerField()
    bath=models.IntegerField()
    area=models.IntegerField()
    garage=models.IntegerField()
    price=models.IntegerField()
    position=models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta():
        ordering=['created_at']
    