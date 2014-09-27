from django.conf.urls import patterns, url

# Authentication
from django.contrib.auth.views import login, logout

from store import views

urlpatterns = patterns('',
    # ex: /store/
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),

    # ex: /store/(?<appid>)
    url(r'^(?P<appid>\d+)', views.detail, name='detail'),

    url(r'^accounts/login/$', login, {'template_name': 'store/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'store/logout.html'}, name='logout'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/profile/(?P<username>[\w]+)$', views.profile_pub, name='profile_pub'),

    # Proxy
    url(r'^proxy/$', views.proxy, name='proxy'),
    # Search
    url(r'^search/$', views.search, name='search'),

    # infinite
    url(r'^infinite/$', views.infinite, name='infinite'),
    url(r'^infinite/json/(?P<page>[0-9]+)/$', views.infinite_json, name='infinite_json'),

)

handler404 = views.http404
handler500 = views.http500
