from django.utils import timezone
from api.models import User
from django.utils.deprecation import MiddlewareMixin


class CheckLastActivityMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())
