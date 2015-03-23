"""middleware"""
from apps.hello.models import RequestData
from django.utils import timezone

class RequestStore(object):
    """
    RequestStore middleware class
    """
    def process_request(self, request):
        """
        store all http requests in the DB
        """
        if request.method == 'POST':
            request_args = request.POST
        else:
            request_args = request.GET

        if 'user' in dir(request) and request.user.username != "":
            username = request.user.username
        else:
            username = 'AnonymusUser'

        requstdata = RequestData(path=request.path, \
                                 method=request.method, \
                                 args=request_args, \
                                 username=username, \
                                 pub_date=timezone.now(), \
                                 )
        requstdata.save()
