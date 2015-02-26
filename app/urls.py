# -*- encoding:utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from api.routers import router

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='pages/landing.html'), name="home"),

    # API urls
    url(r'^api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    # url(r'^accounts/', include('allauth.urls')),

)


def mediafiles_urlpatterns(prefix):
    """
    Method for serve media files with runserver.
    """
    import re
    from django.views.static import serve

    return [
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
            {'document_root': settings.MEDIA_ROOT})
    ]

if settings.DEBUG:
    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")


