from django.shortcuts import redirect

def model_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next={request.path}&required=1")
        return view_func(request, *args, **kwargs)
    return _wrapped_view