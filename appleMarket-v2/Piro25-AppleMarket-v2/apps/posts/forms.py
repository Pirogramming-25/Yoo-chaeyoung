from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'region', 'user', 'price', 'photo',
            'nutrition_image', 'calories', 'carbs', 'protein', 'fat'  # 👈 이 필드들이 모두 들어있어야 합니다!
        ]
        exclude = ['created_at', 'updated_at']