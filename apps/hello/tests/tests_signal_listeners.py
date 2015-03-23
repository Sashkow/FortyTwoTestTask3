from django.test import TestCase

from django.contrib.auth.models import User
from apps.hello.models import Person, RequestData, ModelEntry, models_signals_receiver
from django.db import models

from django.contrib.sites.models import Site

from django.utils import timezone

class ModelsSignalsTestCase(TestCase):
    """
    signal signal listener function that, for every model, creates the db
    entry about the object creation/editing/deletion
    """
    def test_db_upd_on_model_save(self):
        """
        test for each Model that db updates with mode_object each time mode_object is saved
        (works for custom models)
        """        
        from django.db import models
        # models_list = models.get_models(include_auto_created=True)

        models_list = [User, Person, RequestData]
        for ModelClass in models_list:
            if ModelClass.objects.count() > 0:
                model_object = ModelClass.objects.all()[0]
                model_object.save()
                self.assertEquals(len(ModelEntry.objects.filter(
                    model_name=str(ModelClass.__name__),
                    istance_name=str(model_object),
                    instance_pk=model_object.pk)),1)


    def test_db_upd_on_model_create(self):
        """
        test for each Model that db updates with mode_object each time mode_object is saved
        (works for custom models)
        """        
        
        # models_list = models.get_models(include_auto_created=True)
        user = User.objects.create(username='hellosignals')
        self.assertEquals(len(ModelEntry.objects.filter(
            model_name=str(User.__name__),
            istance_name=str(user),
            instance_pk=user.pk,
            event="create")),1)

        person = Person.objects.create(user=user)
        self.assertEquals(len(ModelEntry.objects.filter(
            model_name=str(Person.__name__),
            istance_name=str(person),
            instance_pk=person.pk,
            event="create")),1)

        requestdata = RequestData.objects.create(pub_date=timezone.now())
        self.assertEquals(len(ModelEntry.objects.filter(
            model_name=str(RequestData.__name__),
            istance_name=str(requestdata),
            instance_pk=requestdata.pk,
            event="create")),1)

        model_name=str(Person.__name__)
        istance_name=str(person)
        instance_pk=person.pk

        person.delete()
        self.assertEquals(len(ModelEntry.objects.filter(
            model_name=model_name,
            istance_name=istance_name,
            instance_pk=instance_pk,
            event="delete")),1)

        model_name=str(User.__name__)
        istance_name=str(user)
        instance_pk=user.pk

        user.delete()
        self.assertEquals(len(ModelEntry.objects.filter(
            model_name=model_name,
            istance_name=istance_name,
            instance_pk=instance_pk,
            event="delete")),1)