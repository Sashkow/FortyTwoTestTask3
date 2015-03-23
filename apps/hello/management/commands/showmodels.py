from django.core.management.base import BaseCommand, CommandError
from apps.hello.models import Person

from apps.hello.utils import list_models

class Command(BaseCommand):
    """
    List of all models, known to ORM with amout of objects in them
    """
    def handle(self, *args, **options):
        """
        command's hande method
        """
        # for poll_id in args:
        model_amount_dict = list_models()
        self.stdout.write("List of all models, known to ORM with amout of objects in them")
        for model, amount in model_amount_dict.iteritems():
            writing = "Model %s: %s objects" % (model._meta.module_name, amount)
            self.stdout.write(writing)

        for model, amount in model_amount_dict.iteritems():
            writing = "Model %s: %s objects" % (model._meta.module_name, amount)
            self.stderr.write("error: " + writing)
