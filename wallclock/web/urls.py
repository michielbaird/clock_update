from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('web.views',
            url(r'^$', 'index'), 
            url(r'^settime$', 'set_time'), )
