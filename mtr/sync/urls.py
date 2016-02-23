from .settings import SETTINGS
from django.conf.urls import patterns, url

if SETTINGS['INCLUDE']['API']:
    from .api import SettingsAPI, FieldAPI

    urlpatterns = patterns(
        'mtr.sync.views',

        url(r'^api/settings', SettingsAPI.as_view()),
        url(r'^api/fields', FieldAPI.as_view())
    )
