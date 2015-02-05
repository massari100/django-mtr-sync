from django.conf.urls import patterns, url


urlpatterns = patterns('mtr.sync.views',
    url(r'/', 'dashboard', name='dashboard'),
)
