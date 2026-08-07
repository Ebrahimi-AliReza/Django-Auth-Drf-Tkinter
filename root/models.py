from django.db import models




class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name


class Skills(models.Model):
    title=models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    rating=models.FloatField(default=0)
    def __str__(self):
        return self.title


class Agent(models.Model):
    name=models.CharField(max_length=100)
    photo=models.ImageField(default='agents/default.jpg',upload_to='agents/')
    skill=models.ForeignKey(Skills,on_delete=models.DO_NOTHING)
    twitter=models.URLField(max_length=100,blank=True,null=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['created_at']


    def __str__(self):
        return self.name
    
class Star(models.Model):
    count=models.IntegerField()
    
    def __str__(self):
        return str(self.count)
    
class Testimonial(models.Model):
    name=models.CharField(max_length=150)
    score=models.ForeignKey(Star,on_delete=models.DO_NOTHING)
    photo=models.ImageField(upload_to='testimonials/',default='testimonials/default.jpg')
    position=models.CharField(max_length=100)
    message=models.TextField(max_length=100)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def score_count(self):
        return range(self.score.count)
        