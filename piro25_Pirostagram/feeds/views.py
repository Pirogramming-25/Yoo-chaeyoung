import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Feed, Comment, Story


# Create your views here.
def get_current_user():
    return User.objects.first()

def home(request):
    # 0. 현재 유저 가져오기
    # (로그인 안 된 익명 유저일 때 get_current_user()가 터진다면 request.user를 쓰거나 예외처리가 필요할 수 있습니다.)
    current_user = request.user 

    # 1. 🌟 로그인 상태에 따른 프로필 및 팔로우 데이터 처리 (에러 원천 차단)
    if request.user.is_authenticated:
        try:
            my_profile = request.user.profile
            followed_profiles = my_profile.followings.select_related('user').all()
        except Exception:
            my_profile = None
            followed_profiles = []
    else:
        # 로그인 안 한 유저라면 싹 비워서 아래 반복문들이 에러 없이 통과하게 만듭니다.
        my_profile = None
        followed_profiles = []

    # 2. 팔로우한 유저들의 ID 리스트 추출
    followed_user_ids = [profile.user_id for profile in followed_profiles]

    # 3. 스토리 데이터 가공 (로그인 안 되어 있으면 빈 배열로 패스됨)
    story_users = []
    seen_user_ids = set()
    story_data = []
    
    # filter(__in=[]) 상태가 되므로 쿼리가 터지지 않고 빈 결과만 안전하게 반환됩니다.
    stories_queryset = Story.objects.filter(author_id__in=followed_user_ids).select_related('author__profile').order_by('-id')
    
    for story in stories_queryset:
        if story.author_id in seen_user_ids:
            continue
        seen_user_ids.add(story.author_id)
        user_stories = list(Story.objects.filter(author_id=story.author_id).order_by('id'))
        story_users.append({
            'user': story.author,
            'profile': story.author.profile,
            'latest_story': story,
            'stories': user_stories,
        })
        story_data.append({
            'username': story.author.username,
            'stories': [{'id': s.id, 'image_url': s.image.url} for s in user_stories],
        })

    # 4. 팔로우한 유저들의 피드 데이터 가공 (로그인 안 되어 있으면 패스됨)
    followed_users_data = []
    for profile in followed_profiles:
        user = profile.user
        feeds = Feed.objects.filter(author=user).order_by('-id')
        followed_users_data.append({
            'profile': profile,
            'user': user,
            'feeds': feeds,
            'post_count': feeds.count(),
            'follower_count': profile.followers.count(),
            'following_count': profile.followings.count(),
        })

    # 5. 컨텍스트 구성 후 템플릿 렌더링
    context = {
        'current_user': current_user,
        'my_profile': my_profile,
        'story_users': story_users,
        'story_data_json': json.dumps(story_data),
        'followed_users_data': followed_users_data,
    }

    return render(request, 'feeds/home.html', context)

def feed_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        content = request.POST.get('content', '').strip()

        if image and content:
            feed = Feed.objects.create(author=get_current_user(), image=image, content=content)

        return redirect('feeds:home')
    return render(request, 'feeds/feed_form.html')


def feed_detail(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)

    context = {
        'feed': feed,
        'current_user': get_current_user(),
    }

    return render(request, 'feeds/feed_detail.html', context)


def feed_update(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    if request.method == 'POST':
        new_image = request.FILES.get('image')
        if new_image:
            feed.image = new_image

        feed.content = request.POST.get('content', '').strip()

        feed.save()
        return redirect('feeds:feed_detail', feed_id=feed_id)
    
    return render(request, 'feeds/feed_form.html', {'feed': feed})


def feed_delete(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    feed.delete()

    return redirect('feeds:home')


def feed_like(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    me = get_current_user()
    
    if feed.like_users.filter(id=me.id).exists():
        feed.like_users.remove(me)
    else:
        feed.like_users.add(me)

    previous_url = request.META.get('HTTP_REFERER')
    
    if previous_url:
        return redirect(previous_url)
    
    return redirect('feeds:home')


def comment_create(request, feed_id):
    if request.method == 'POST':
        feed = get_object_or_404(Feed, id=feed_id)
        content = request.POST.get('content', '').strip()
        
        if content:
            Comment.objects.create(feed=feed, author=get_current_user(), content=content)

    return redirect('feeds:feed_detail', feed_id=feed_id)


def comment_update(request, feed_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.content = request.POST.get('content', comment.content).strip()
        comment.save()
        
    return redirect('feeds:feed_detail', feed_id=feed_id)


def comment_delete(request, feed_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect('feeds:feed_detail', feed_id=feed_id)


def story_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            Story.objects.create(author=get_current_user(), image=image)
        return redirect('feeds:home')
        
    return render(request, 'feeds/story_form.html')

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    return render(request, 'feeds/story_detail.html', {'story': story})