from django.shortcuts import redirect
from django.urls import reverse

class GroupRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/wizard/') and not request.user.is_authenticated:
            return redirect(reverse('CustomLoginView'))

        if request.path.startswith('/wizard/') and not request.user.groups.filter(name='member').exists():
            return redirect(reverse('CustomLoginView'))

        response = self.get_response(request)
        return response
