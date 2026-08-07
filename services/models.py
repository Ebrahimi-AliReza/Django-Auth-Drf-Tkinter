from django.db import models

class Tags(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Specials(models.Model):
    title=models.TextField(max_length=200)
    def __str__(self):
        return self.title
    
    
class Services(models.Model):
    title=models.CharField(max_length=35)
    tags=models.ManyToManyField(Tags)
    short_content=models.CharField(max_length=75)
    category=models.ManyToManyField(Category)
    catalog=models.URLField(default='maktabkhooneh.org')
    description=models.TextField(max_length=500)
    specials=models.ManyToManyField(Specials,)
    photo=models.ImageField(default='services/default.png',upload_to='services')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta():
        ordering=['created_at']
    