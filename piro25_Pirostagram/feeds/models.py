from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feed(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')

    image = models.ImageField(upload_to='feeds/')

    content = models.TextField()

    like_users = models.ManyToManyField(User, related_name='liked_feeds', blank=True)

    def __str__(self):
        return f"{self.author.username} Feed ({self.id})"
    

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='comments')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()

    def __str__(self):
        return f"{self.author.username} Comment ({self.id})"
    
    
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')

    image = models.ImageField(upload_to='stories/')

    def __str__(self):
        return f"{self.author.username} Story ({self.id})"