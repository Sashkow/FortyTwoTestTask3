from django.test import TestCase

from django.core.management import call_command

from django.core.management import call_command
from StringIO import StringIO 
 
from django.contrib.auth.models import User
from apps.hello.models import Person, RequestData

import os
from django.conf import settings

import subprocess

import datetime


class ShowModelsCommandTestCase(TestCase):
    """
    Test case for commmand that prints all project models and the count of
    objects in every model
    """
    def setUp(self):
        subprocess.call(['./showmodels.sh'])

    def test_runs(self):
      """
      test command runs without errors in bash
      """
      try:
          call_command('showmodels', 'foo', bar='baz')
      except Exception, e:
          self.fail("command run failed: %s" % e)

    def test_contains_correct_output(self):
        """
        test command shows list all models known to ORM and amounts of objecs
        stored in them 
        """
        content = StringIO()
        call_command("showmodels", stdout=content)
        content.seek(0)
        output_string = content.read()

        self.assertTrue("user: %s" % User.objects.count() in output_string)

        self.assertTrue("person: %s" % 
        Person.objects.count() in output_string)

        self.assertTrue("requestdata: %s" %
        RequestData.objects.count() in output_string)

    def test_stderr_contains_correct_output(self):
        """
        test command shows list all models known to ORM and amounts of objecs
        stored in them 
        """
        content = StringIO()
        call_command("showmodels", stderr=content)
        content.seek(0)
        output_string = content.read()

        self.assertTrue("error: Model user: %s" %
        User.objects.count() in output_string)

        self.assertTrue("error: Model person: %s" %
        Person.objects.count() in output_string)

        self.assertTrue("error: Model requestdata: %s" %
        RequestData.objects.count() in output_string)

    def test_bash_file_exists(self):
        """
        test bash script file that executes showmodels command exists
        """
        self.assertTrue('showmodels.sh' in os.listdir(settings.BASE_DIR))

    def test_bash_file_exists(self):
        """
        test bash script file that executes showmodels command exists
        """
        self.assertTrue('showmodels.sh' in os.listdir(settings.BASE_DIR))

    def test_bash_file_creates_dat(self):
        """
        test bash creates a file  with current date as name and .dat as extention
        """
        file_name = ('%s.dat' % datetime.date.today()).replace('-','_')
        self.assertTrue(file_name in os.listdir(settings.BASE_DIR))     

    def test_bash_file_creates_dat(self):
        """
        test bash file saves output of stderr into file
        """
        file_name = ('%s.dat' % datetime.date.today()).replace('-','_')
        with open(file_name,'r') as f:
            self.assertTrue("error: Model user" in f.read())
        




