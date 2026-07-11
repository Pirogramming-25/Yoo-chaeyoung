from django.contrib.auth.models import User
from .models import Profile


def sidebar_user(request):
    user = User.objects.first()
    if not user:
        return {'current_user': None, 'my_profile': None}
    profile, _ = Profile.objects.get_or_create(user=user)
    return {'current_user': user, 'my_profile': profile}
