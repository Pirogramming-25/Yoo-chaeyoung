from django.db import models
from django.contrib.auth.models import User
from devtools.models import Devtool

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='idea_pics')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(Devtool, on_delete=models.SET_NULL, null=True, blank=True, related_name='ideas')

    def __str__(self):
        return self.title
    
class IdeaStar(models.Model):
    idea = models.OneToOneField('Idea', on_delete=models.CASCADE, related_name='star_status')
    is_starred = models.BooleanField(default=False)