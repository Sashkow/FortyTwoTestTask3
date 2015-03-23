"""
hello app views
"""
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from apps.hello.models import Person, RequestData, ModelEntry

from apps.hello.forms import PersonForm

from apps.hello.utils import get_person_or_admin

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate
from django.contrib import auth

import json
from django.utils import simplejson


def main(request):
    """
    A view that presents my name, surname, date of birth, bio, contacts
    on the main page.
    """
    person = get_person_or_admin(request)
    
    # if hasattr(person.ava,'url'):
    #     ava_url = person.ava.url
    # else:
    #     ava_url = ""
    # print person.ava.thumbnail.url
    return render(request, "hello/index.html", \
     {'person': person})

def requests(request):
    """
    A view that shows first 10 http requests that are stored by middleware
    """
    shown_requests_count = 10
    template_name = 'hello/requests.html'
    requests = RequestData.objects.all()[:shown_requests_count]
    context = {'requests': requests}
    return render(request, template_name, context)

def edit(request):
    """
    A view that allows to edit content from 'main' view
    """

    person = get_person_or_admin(request)

    if request.method == 'POST':
        # post = request.POST.copy()
        # post['user'] = person.user.pk
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
        else:
            return render(request, "hello/edit.html", 
            {'form': form, 'person': person})

        return HttpResponseRedirect(reverse('main'))
    else:
        form = PersonForm(instance=person)
        # print form['email']
        # print form['birth_date']
    
    return render(request, "hello/edit.html", 
     {'form': form, 'person': person})

def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )

def json_response(x):
    import json
    return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json')
def edit_ajax(request):
    """
    a view that allows to save content of the main page without
    refreshing the page
    """
    if request.method == 'POST':
        
        person = Person.objects.get(user=request.user)
        
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
        else:
            return json_response({
                    'success': False,
                    'errors': errors_to_json(form.errors),
                    })

        person = Person.objects.get(user=request.user)

        if hasattr(person.ava, 'thumbnail'):
            img_url = person.ava.thumbnail.url
        else:
            img_url = "/static/hello/img/default_ava.png"



        return HttpResponse(
                json.dumps({
                    'success': True,
                    'img_url': img_url,

                    }),
                content_type="application/json"
            )

    return HttpResponse("You shouldn't have come here.")

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
        return HttpResponseRedirect(reverse('main'))
    else:
        form = AuthenticationForm()
    return render(request, 'hello/login.html', {'form': form})    

