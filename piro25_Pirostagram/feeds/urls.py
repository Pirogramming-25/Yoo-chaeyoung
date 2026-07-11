from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    # 메인 홈 피드 화면
    path('', views.home, name='home'),

    # 게시글 작성, 수정 및 삭제, 디테일
    path('feed/create/', views.feed_create, name='feed_create'),
    path('feed/<int:feed_id>/', views.feed_detail, name='feed_detail'),
    path('feed/<int:feed_id>/update/', views.feed_update, name='feed_update'),
    path('feed/<int:feed_id>/delete/', views.feed_delete, name='feed_delete'),

    # 게시글 좋아요 기능
    path('feed/<int:feed_id>/like/', views.feed_like, name='feed_like'),

    # 게시글 댓글 작성, 수정, 삭제
    path('feed/<int:feed_id>/comment/create/', views.comment_create, name='comment_create'),
    path('feed/<int:feed_id>/comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('feed/<int:feed_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    
    # 스토리 작성
    path('story/create/', views.story_create, name='story_create'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail')
]