from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    profile_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)

    bio = models.TextField(blank=True, default="소개글이 없습니다.")

    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"