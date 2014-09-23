from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'playstore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', include('store.urls', namespace='store')),
    url(r'^comments/', include('django.contrib.comments.urls')),


)

