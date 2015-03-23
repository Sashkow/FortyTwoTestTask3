from django.test import TestCase
from django.template import Template, Context

from django.contrib.auth.models import User, AnonymousUser
from apps.hello.models import Person, RequestData

from django.core.urlresolvers import reverse

class EditLinkTestCase(TestCase):
    """
    Test case for edit_link template tag
    """
        
    def test_user_loads_and_renders(self):
        """
        test tag does not raise error when loaded and used
        """
        user = User.objects.get(username = 'admin')
        try:
            template = '{% load edit_link %}{% edit_link object %}'
            context = {'object': user}
            rendered = Template(template).render(Context(context))
        except:
            self.fail("raised exception while template rendering")
        self.assertEquals(rendered, '<a href="/admin/auth/user/%s/">(admin)</a>' % str(user.pk))

    def test_person_loads_and_renders(self):
        """
        test tag does not raise error when loaded and used
        """
        person = Person.objects.get(user__username = 'admin')
        try:
            template = '{% load edit_link %}{% edit_link object %}'
            context = {'object': person}
            rendered = Template(template).render(Context(context))
        except:
            self.fail("raised exception while template rendering")
        self.assertEquals(rendered, '<a href="/admin/hello/person/%s/">(admin)</a>' % str(person.pk))

    def test_person_loads_and_renders(self):
        """
        test tag does not raise error when loaded and used
        """
        response = self.client.get(reverse('main'))
        request_data = RequestData.objects.latest('pub_date')
        try:
            template = '{% load edit_link %}{% edit_link object %}'
            context = {'object': request_data}
            rendered = Template(template).render(Context(context))
        except:
            self.fail("raised exception while template rendering")
        self.assertEquals(rendered, '<a href="/admin/hello/requestdata/%s/">(admin)</a>' % str(request_data.pk))



    
        