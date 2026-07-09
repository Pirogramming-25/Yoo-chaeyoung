from django.db import models

# Create your models here.
class Devtool(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name