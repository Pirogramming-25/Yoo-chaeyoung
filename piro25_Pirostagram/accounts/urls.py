from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 프로필 확인
    path('profile/<int:user_id>/', views.profile, name='profile'),

    # 프로필 팔로우
    path('profile/<int:user_id>/follow/', views.follow, name='follow'),

    # 프로필 검색
    path('search/', views.user_search, name='user_search')
]