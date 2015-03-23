from django.conf.urls import patterns, url
from apps.hello import views

urlpatterns = patterns('',
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^main/$', views.main, name='main'),
    url(r'^edit/edit_ajax/$', views.edit_ajax, name='edit-ajax'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^login/$', views.login, name='login'),
)

