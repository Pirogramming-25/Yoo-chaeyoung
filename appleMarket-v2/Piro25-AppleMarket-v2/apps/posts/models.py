from django.db import models
from django.utils import timezone
from apps.users.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField('제목', max_length=20)
    content = models.CharField('내용', max_length=20)
    region = models.CharField('지역', max_length=20)
    user = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    price = models.IntegerField('가격', default=1000)
    photo = models.ImageField('이미지', blank=True, upload_to='posts/%Y%m%d')

    nutrition_image = models.ImageField(upload_to='nutrition/', null=True, blank=True)
    calories = models.FloatField(null=True, blank=True) # 칼로리 (kcal)
    carbs = models.FloatField(null=True, blank=True)    # 탄수화물 (g)
    protein = models.FloatField(null=True, blank=True)  # 단백질 (g)
    fat = models.FloatField(null=True, blank=True)      # 지방 (g)
    
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:  # 수정일 때에만 갱신
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)