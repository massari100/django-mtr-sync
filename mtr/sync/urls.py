from .settings import SETTINGS
from django.conf.urls import url

if SETTINGS['INCLUDE']['API']:
    from .api import SettingsAPI, FieldAPI

    urlpatterns = (
        url(r'^api/settings', SettingsAPI.as_view()),
        url(r'^api/fields', FieldAPI.as_view())
    )
