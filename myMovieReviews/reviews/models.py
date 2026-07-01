from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.CharField(max_length=20)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    running_time = models.CharField(max_length=30)
    content = models.TextField()
    director = models.CharField(max_length=50)
    actor = models.CharField(max_length=200)

    def __str__(self):
        return self.title