from django.test import TestCase

from django.core.urlresolvers import reverse
# from django.test import Client
from django.test.client import RequestFactory

from apps.hello.models import Person, RequestData
from django.contrib.auth.models import User

import os
from django.conf import settings

from django.utils import timezone

class PersonModelTestCase(TestCase):
    """
    test Person model
    """
    # fixtures = ['test_data.json']

    def test_person__str__(self):
        """
        test __str__ method returns first_name last_name
        """

        user = User.objects.get(username='admin')
        person = Person(user=user)
        self.assertEquals(person.__str__(), "Olexandr Lykhenko")

    def test_person_properties_change_user(self):
        """
        test getter and setter for name, surname, email peroperties
        test :model:`hello.Person` change affects :model:`auth.User` change
        """
        user = User.objects.get(username='admin')
        person = Person.objects.get(user=user)
        self.assertEquals(person.name, "Olexandr")
        self.assertEquals(person.surname, "Lykhenko")
        self.assertEquals(person.email, "lykhenko.olexandr@gmail.com")
        person.name = "Ololoshka"
        person.surname = "Trololo"
        person.email = "ololo@lol.lol"
        self.assertEquals(person.name, "Ololoshka")
        self.assertEquals(person.surname, "Trololo")
        self.assertEquals(person.email, "ololo@lol.lol")

        self.assertEquals(user.first_name, "Olexandr")
        self.assertEquals(user.last_name, "Lykhenko")
        self.assertEquals(user.email, "lykhenko.olexandr@gmail.com")

        person.save() #save person also saves user

        user = User.objects.get(username='admin')
        self.assertEquals(user.first_name, "Ololoshka")
        self.assertEquals(user.last_name, "Trololo")
        self.assertEquals(user.email, "ololo@lol.lol")



class RequestDataTestCase(TestCase):
    # fixtures = ['test_data.json']
    def test__str__(self):
        """
        test __str__ outputs verbose object description
        """
        self.client.get(reverse('main'))
        requestdata = RequestData.objects.latest('pub_date')
        self.assertTrue("path:/ method:GET args:<QueryDict: {}> \
username:AnonymusUser" in requestdata.__str__())

    def test_default_priority_in_new_record(self):
        """
        test new record of database will contain priority with default value 0
        """
        requestdata = RequestData(pub_date=timezone.now())
        requestdata.save()
        self.assertTrue(hasattr(requestdata,"priority"))
        self.assertEquals(requestdata.priority,0)

    def test_records_ordered_by_priority(self):
        """
        test records are ordered by priority decending and then - by date
        decending
        """
        for i in range(5):
            RequestData.objects.create(pub_date=timezone.now())

        for i in range(5,0,-1):
            RequestData.objects.create(pub_date=timezone.now(), priority=i)

        requestdatas = RequestData.objects.all()
        priorities = [record.priority for record in requestdatas]
        self.assertTrue(sorted(priorities, reverse=True) == priorities)

        dates_for_priority_0 = [record.pub_date for record in requestdatas if
                                record.priority == 0]
        self.assertTrue(sorted(dates_for_priority_0, reverse=True) == 
            dates_for_priority_0)
