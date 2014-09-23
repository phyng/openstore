from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.conf import settings

from store.models import App, Comments

from zlib import crc32
from PIL import Image
from StringIO import StringIO
import pathlib
import re

# for img proxy
import requests
import redis

# for qiniu
import qiniu.conf
import qiniu.rs
import qiniu.io
qiniu.conf.ACCESS_KEY = settings.QINIU_AK
qiniu.conf.SECRET_KEY = settings.QINIU_SK


def index(request):
    applist_new = App.objects.order_by('id')[:20]
    applist_top = App.objects.filter(
        ratingCount__gt=1000).order_by('ratingValue').reverse()[:20]
    applist_topdownload = App.objects.order_by('ratingCount').reverse()[:20]

    # applist_new
    new_applist_new = []
    for app in applist_new:
        app.icon = proxy_img(app.icon)
        new_applist_new.append(app)
    # applist_top
    new_applist_top = []
    for app in applist_top:
        app.icon = proxy_img(app.icon)
        new_applist_top.append(app)
    # applist_topdownload
    new_applist_topdownload = []
    for app in applist_topdownload:
        app.icon = proxy_img(app.icon)
        new_applist_topdownload.append(app)

    # render
    template = loader.get_template('store/index.html')
    context = Context({
        'applist_new': new_applist_new,
        'applist_top': new_applist_top,
        'applist_topdownload': new_applist_topdownload,
        'user': request.user,

    })
    return HttpResponse(template.render(context))


def about(request):
    return render(request, 'store/about.html')


def detail(request, appid):
    # verify appid
    try:
        app = App.objects.get(appid=appid)
    except App.DoesNotExist:
        raise Http404

    # Add comments
    if request.method == "POST":
        if request.user.is_authenticated():

            comments = request.POST['comments']
            c = Comments(appid=int(appid),
                         date=timezone.now(),
                         username=request.user.username,
                         comments=comments)
            c.save()
            return HttpResponseRedirect('/store/%s' % str(appid))
        else:
            return HttpResponseRedirect('/store/accounts/login')

    # get comments
    comments = Comments.objects.filter(appid=appid)

    path = settings.STATICFILES_DIRS[0] + '/img/'

    # app.icon

    app.icon = proxy_img(app.icon)

    # img_list
    img_list = [i for i in app.get_img_list()]

    new_img_ilst = [proxy_img(img_list[i]) for i in range(len(img_list))]

    return render(request,
                  'store/detail.html',
                  {'app': app,
                   'user': request.user,
                   'img_list': new_img_ilst,
                   'comments': comments})


def profile(request):
    if request.user.is_authenticated():
        comments = Comments.objects.filter(username=request.user.username)
        return render(request,
                      'store/profile.html',
                      {'user': request.user, 'comments': comments})
    else:
        return HttpResponseRedirect('/store/accounts/login')


def profile_pub(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    comments = Comments.objects.filter(username=username)

    return render(request, 'store/profile_pub.html', {'user': user,
                                                      'comments': comments})


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/store/accounts/profile")
    else:
        form = UserCreationForm()
    return render_to_response("store/register.html",
                              {'form': form},
                              context_instance=RequestContext(request))


def proxy(request):
    if request.GET['url']:
        url = request.GET['url']
        if not re.match(r'^https://\w\w\d.ggpht.com/', url):
            raise Http404
        url = url.replace('/w100', '').replace('/w250', '')

        filename = str(hex(crc32(url) & 0xffffffff))[2:] + ".png"
        reds = redis.StrictRedis(host='localhost', port=6379, db=0)
        exists = reds.get(filename)

        headers = {'accept-language': 'zh_cn', 'accept': 'image/png'}
        session = requests.session()
        # for shadowsocks
        # if settings.DEBUG:
        #    session.proxies = {'https': 'socks5://127.0.0.1:1081'}
        r = session.get(url, headers=headers, timeout=10)
        bitdata = StringIO(r.content)

        if not exists:
            policy = qiniu.rs.PutPolicy('playstore')
            uptoken = policy.token()
            extra = qiniu.io.PutExtra()
            extra.mime_type = "image/png"
            key = filename
            ret, err = qiniu.io.put(uptoken, key, bitdata, extra)
            if not err:
                reds.set(filename, 0)
                return HttpResponseRedirect(settings.QINIU_URL + filename)
            else:
                return Http404  # redirect
        else:
            return HttpResponseRedirect(settings.QINIU_URL + filename)
        # return HttpResponse(bitdata, content_type="image/png")

    else:
        return Http404


def proxy_img(url):

    filename = str(hex(crc32(url) & 0xffffffff))[2:] + ".png"

    reds = redis.StrictRedis(host='localhost', port=6379, db=0)
    exists = reds.get(filename)

    if exists:
        return settings.QINIU_URL + filename

    else:
        return '/store/proxy?url=' + url


def http404(request):
    error = {'code':404,
             'msg': 'Page Not Found.'}
    return render(request, 'store/404.html', {'error':error})

def http500(request):
    error = {'code':500,
             'msg': 'Server Error.'}
    return render(request, 'store/500.html', {'error':error})
