from django.conf.urls import patterns, include, url

from django.contrib import admin
from apps.hello import views

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/', include('apps.hello.urls')),

    url(r'^$', views.main, name='main'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# urlpatterns += patterns('',
#     (r'^ajax-upload/', include('ajax_upload.urls')),
# )