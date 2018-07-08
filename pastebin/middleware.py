import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token


class TokenMiddlewareCheck(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        if request.auth is not None:
            f = datetime.datetime.now()
            print(request.auth.created)
            print(f)
            tf = f - request.auth.created.replace(tzinfo=None)
            print(tf)
            time_difference_in_minutes = tf.total_seconds() / 60
            try:
                lifespan = settings.EXPIRING_TOKEN_LIFESPAN
            except AttributeError:
                lifespan = 5  # The token has 5 minutes to be in use
            if time_difference_in_minutes > lifespan:
                Token.delete(request.auth)
                return HttpResponse(content='{"detail":"Token has expired"}', content_type='application/json', status=401)
        # Code to be executed for each request/response after
        # the view is called.

        return response
