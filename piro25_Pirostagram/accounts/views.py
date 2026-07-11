from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from feeds.models import Feed
from .models import Profile


# Create your views here.
def get_current_user():
    return User.objects.first()


def profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile, _ = Profile.objects.get_or_create(user=target_user)

    my_user = get_current_user()
    my_profile, _ = Profile.objects.get_or_create(user=my_user)

    feeds = Feed.objects.filter(author=target_user).order_by('-id')

    context = {
        'target_user': target_user,
        'target_profile': target_profile,
        'my_profile': my_profile,
        'is_own_profile': target_user.id == my_user.id,
        'is_following': my_profile.followings.filter(id=target_profile.id).exists(),
        'feeds': feeds,
        'post_count': feeds.count(),
        'follower_count': target_profile.followers.count(),
        'following_count': target_profile.followings.count(),
    }
    return render(request, 'accounts/profile.html', context)


def follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile = target_user.profile

    my_user = get_current_user()
    my_profile = my_user.profile

    is_following = False
    if my_profile != target_profile:
        if my_profile.followings.filter(id=target_profile.id).exists():
            my_profile.followings.remove(target_profile)
        else:
            my_profile.followings.add(target_profile)
            is_following = True

    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect('accounts:profile', user_id=user_id)


def user_search(request):
    search_username = request.GET.get('search_username', '').strip()

    my_user = get_current_user()
    my_profile, _ = Profile.objects.get_or_create(user=my_user)

    if search_username:
        searched_users = User.objects.filter(username__icontains=search_username).exclude(id=my_user.id)
    else:
        searched_users = User.objects.none()

    users_data = []
    for user in searched_users:
        profile, _ = Profile.objects.get_or_create(user=user)
        users_data.append({
            'user': user,
            'profile': profile,
            'is_following': my_profile.followings.filter(id=profile.id).exists(),
        })

    context = {
        'search_username': search_username,
        'users_data': users_data,
    }
    return render(request, 'accounts/search_result.html', context)