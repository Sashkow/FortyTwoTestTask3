import os
from django.conf import settings

from django.test import TestCase
from django.core.urlresolvers import reverse

from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from apps.hello.models import Person, RequestData

from django.contrib.sessions.middleware import SessionMiddleware

from apps.hello.utils import get_person_or_admin, list_models

def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save() 

class GetPersonOrAdminUtilTestCase(TestCase):
    """
    test util function that gets Person object for current User if
    authenticated or logins as admin and then gets Person object for admin 
    """
    # fixtures = ['test_data.json']

    def setUp(self):
        self.factory = RequestFactory()

    def test_gets_admin_if_unauthed(self):
        """
        test function returns Person object for admin
        if user is not authenticated
        """
        request = self.factory.get(reverse('main'))
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEquals(get_person_or_admin(request).user.username,'admin')

    def test_gets_person_if_authed(self):
        """
        test function returns Person obect for user
        if user is authenticated
        """
        request = self.factory.get(reverse('main'))
        request.user = User.objects.get(username='leela')
        self.assertEquals(get_person_or_admin(request).user.username,'leela')


class FixtureTestCase(TestCase):
    """
    test fixture behavior
    """
    def test_fixture_files_exist(self): 
        """
        test fixture media files exist in media folder
        """
        fixture_persons_dir = os.listdir(settings.MEDIA_ROOT + '/fixture_persons')
        self.assertTrue('2014-10-12-214256.jpg' in fixture_persons_dir)
        self.assertTrue('2014-10-12-214256.thumbnail.jpg' in fixture_persons_dir)

    def test_objects_in_models(self):
        """
        test proper ojbects loaded from fixtures
        """
        self.assertEquals(User.objects.filter(username='admin').count(),1)
        self.assertEquals(User.objects.filter(username='leela').count(),1)
        self.assertEquals(Person.objects.filter(user__username='admin').count(),1)
        self.assertEquals(Person.objects.filter(user__username='leela').count(),1)


class ListModelsTestCase(TestCase):
    """
    function, which produces list of model-user tuples for each model,
    contains correct data about Person, User
    """
    def test_returns_correct_data(self):
        """
        test function contains correct data about project models' counts
        """
        dct = list_models()
        self.assertTrue(User in dct)
        self.assertTrue(Person in dct)
        self.assertTrue(RequestData in dct)

        self.assertEquals(dct[User], User.objects.count())
        self.assertEquals(dct[Person], Person.objects.count())
        self.assertEquals(dct[RequestData], RequestData.objects.count())
