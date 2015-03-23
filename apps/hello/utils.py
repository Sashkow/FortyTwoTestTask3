from django.contrib.auth import authenticate
from django.contrib import auth

from apps.hello.models import Person


def get_person_or_admin(request):
    """
    get Person object for current User if authenticated
    or
    login as admin and then get Person object for admin 
    """
    user = request.user
    if not user.is_authenticated():
        user = authenticate(username='admin', password='admin')
        auth.login(request, user)

    return Person.objects.get(user__username=user.username)

def list_models():
    from django.db import models
    models_list =  models.get_models(include_auto_created=True)
    model_amount_dict = { model: model.objects.count() for model in models_list} 
    return model_amount_dict

    
