from django.test import TestCase

from django.core.urlresolvers import reverse
# from django.test import Client
from django.test.client import RequestFactory

from django.conf import settings


class AddDjangoSettingsContextProcessorTestCase(TestCase):
    """
    Test case for template context processor that adds
    django.settings to context
    """
    # fixtures = ['test_data.json']
    def test_djago_settings_in_context(self):
        """
        test django_settings variable available from context
        """
        response = self.client.get(reverse('main'))
        self.assertTrue('django_settings' in response.context)

    def test_correct_django_settings_in_context(self):
        """
        test django settings context variable data matches settings data
        """
        response = self.client.get(reverse('main'))
        self.assertEquals(response.context['django_settings'], settings)

