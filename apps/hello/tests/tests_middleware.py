from django.test import TestCase

from django.core.urlresolvers import reverse
# from django.test import Client
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from apps.hello.models import RequestData
from apps.hello.middleware import RequestStore


class RequestStoreMiddlewareTestCase(TestCase): 
    """
    RequestStore middleware test case
    """
    # fixtures = ['test_data.json']
    def setUp(self):
        self.factory = RequestFactory()

    def test_middleware_updates_database(self):
        """
        test whether :model:`RequestData` amount is increased when request 
        is made (functional test)
        """
        requestdata_count = len(RequestData.objects.all())

        self.client.get('fake/url')

        self.assertTrue(len(RequestData.objects.all()) > requestdata_count)

    def test_middleware_updates_database_correctly(self):
        """
        test data in :model:`RequestData` matches actual request 
        """
        
        request = self.factory.get('fake/url', {'number': '6'})
        request.user = User.objects.get(username='admin')
        requeststore = RequestStore()
        requeststore.process_request(request)
        requestdata = RequestData.objects.latest('pub_date')

        self.assertEquals(request.path, requestdata.path)
        self.assertEquals(request.method, requestdata.method)
        self.assertEquals(str(request.GET), requestdata.args)
        self.assertEquals('admin', requestdata.username)
