from django.test import TestCase

from django.core.urlresolvers import reverse
# from django.test import Client
from django.test.client import RequestFactory

from apps.hello.models import Person
from django.contrib.auth.models import User

from apps.hello.forms import PersonForm

from django.conf import settings
from django.conf.urls.static import static

from apps.hello.utils import get_person_or_admin

import os

class PersonFormTestCase(TestCase):
    """
    test PersonForm modelform from admin.py
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_form_gets_values_from_instance_user_on_init(self):
        """
        test that, given instance, form retreives name, surname, email
        values from instance.user and sets initial values of corresponding
        fields on __init__ form
        """
        user = User.objects.get(username='admin')
        person = Person(user=user)
        personform = PersonForm(instance=person)
        personfields_wishdict = {'name': 'Olexandr',
                                 'surname': 'Lykhenko',
                                 'email': 'lykhenko.olexandr@gmail.com',
                                }

        self.assertTrue(all(item in personform.initial.items() \
                        for item in personfields_wishdict.items()))

    def test_saves_user_on_save(self):
        """
        test that, form saves name, surname, email values to corresponding User
        when commiting form
        """
        person = Person.objects.get(user__username='admin')
        personform = PersonForm(instance=person, data={'user': person.user.pk, 'name': 'has_changed'})
        
        if personform.is_valid():
            person = personform.save()
            self.assertEquals(User.objects.get(pk=person.user.pk).first_name, \
             "has_changed")
        else:
            self.fail(personform.errors)
            # self.fail("personform not valid")

    def test_image_uploads_on_save(self):
        """
        test image uploads on form save
        """
        
        files_count = len(os.listdir(settings.MEDIA_ROOT + '/persons'))
        with open('media/test_images/test.jpg') as f:
            self.client.post(reverse('edit'), {'ava': f})
        files_count_after = len(os.listdir(settings.MEDIA_ROOT + '/persons'))
        # added file and thumbnail
        self.assertEquals(files_count_after - files_count, 2) 
        
        # test image scales  
        from PIL import Image
        im = Image.open(settings.MEDIA_ROOT + '/persons/test.thumbnail.jpg')
        thumbnail_size = Person.thumbnail_size
        self.assertEquals((thumbnail_size,thumbnail_size), im.size)
