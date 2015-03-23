"""
app hello models
"""
from django.db import models
from django.contrib.auth.models import User

from stdimage import StdImageField

from django.core.signals import Signal
from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Person(models.Model):
    """
    Model to store my name, surname, date of birth, bio,
    contacts in access to :model:`auth.User` fields provided via properties
    """
    thumbnail_size = 200

    user = models.OneToOneField(User)

    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)
    jabber = models.CharField(max_length=50, null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    ava = StdImageField(null=True, blank=True, upload_to='persons', \
        variations={'thumbnail': {'height': thumbnail_size,
                                   'width': thumbnail_size,
                                    'crop': True}})

    @property
    def name(self):
        return self.user.first_name
    @name.setter
    def name(self, value):
        self.user.first_name = value

    @property
    def surname(self):
        return self.user.last_name
    @surname.setter
    def surname(self, value):
        self.user.last_name = value

    @property
    def email(self):
        return self.user.email
    @email.setter
    def email(self, value):
        self.user.email = value

    def __str__(self):

        return " ".join([self.name, self.surname])

    def save(self, *args, **kwargs):
        """
        override: delete old file when replacing by updating the file
        """
        
        self.user.save() # important:model affects user

        # replace images instead of adding
        try:
            this = Person.objects.get(id=self.id)
            if this.ava != self.ava:
                this.ava.delete(save=False)
        except: pass 
        super(Person, self).save(*args, **kwargs)


class RequestData(models.Model):
    class Meta:
        """
        RequestModelMeta class
        """
        ordering = ('-priority', '-pub_date')

    path = models.CharField(max_length=2000, null=True, blank=True)
    method = models.CharField(max_length=4, null=True, blank=True)
    args = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    priority = models.PositiveIntegerField(default=0)

    def __str__(self):
        return " ".join([str(field.name) + ":" + \
         str(getattr(self, field.name)) for field in self._meta.fields])


class ModelEntry(models.Model):
    model_name = models.CharField(max_length=79, null=True, blank=True)
    istance_name = models.TextField(null=True, blank=True)
    instance_pk = models.PositiveIntegerField(null=True, blank=True)
    event = models.CharField(max_length=10, null=True, blank=True)
    

    def __str__(self):
        return " ".join([self.model_name, self.istance_name, str(self.instance_pk), self.event])


from functools import wraps
from django.db import connection


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            print "Skipping signal for %s %s" % (args, kwargs)
            return
        signal_handler(*args, **kwargs)
    return wrapper


@disable_for_loaddata
def models_signals_receiver(sender, instance, created, **kwargs):
    ### surpress endless recursion
    if sender==ModelEntry:
        return

    # print sender
    ### if table for ModelEntry is ready
    tables = connection.introspection.table_names()
    if  ModelEntry._meta.db_table in tables:
        if created ==True:
            event = "create"
        else:
            event = "save"

        modelentry = ModelEntry(
            model_name=str(sender.__name__),
            istance_name=str(instance),
            instance_pk=instance.pk,
            event=event)
        modelentry.save()


def models_signals_receiver_delete(sender, instance, **kwargs):
    ### surpress endless recursion
    if sender==ModelEntry:
        return

    # print sender
    ### if table for ModelEntry is ready
    tables = connection.introspection.table_names()
    if  ModelEntry._meta.db_table in tables:
        modelentry = ModelEntry(
            model_name=str(sender.__name__),
            istance_name=str(instance),
            instance_pk=instance.pk,
            event="delete")
        modelentry.save()





from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from apps.hello.models import Person
from south.models import MigrationHistory 

# models_list = models.get_models(include_auto_created=True)
models_list = [User, ModelEntry, Person, RequestData]
for ModelClass in models_list:
    post_save.connect(models_signals_receiver, sender=ModelClass)

for ModelClass in models_list:
    post_delete.connect(models_signals_receiver_delete, sender=ModelClass)

