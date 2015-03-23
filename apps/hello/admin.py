from django.contrib import admin
from apps.hello.models import Person, RequestData, ModelEntry
from apps.hello.forms import AdminPersonForm


class PersonAdmin(admin.ModelAdmin):
    """
    overriden :model:`hello.Person` ModelAdmin class show some
    :model:`auth.User`'s fields in context of :model:`hello.Person`'s
    admin change form
    """

    list_display = ('user', 'name', 'surname', 'birth_date', \
     'bio', 'email', 'jabber', 'skype', 'contacts', 'ava')
    fields = ['user','name', 'surname', 'birth_date', \
     'bio', 'email', 'jabber', 'skype', 'contacts', 'ava']

    form = AdminPersonForm


class RequestDataAdmin(admin.ModelAdmin):
    """
    overriden RequestData ModelAdmin class
    """

    list_display = ('id', 'method', 'args', 'username', \
     'pub_date', 'priority')

    ordering = ('-priority', '-pub_date')


admin.site.register(Person, PersonAdmin)
admin.site.register(RequestData, RequestDataAdmin)
admin.site.register(ModelEntry)
