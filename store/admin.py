from django.contrib import admin

# Register your models here.
from store.models import Applist, App, Comments


class ApplistAdmin(admin.ModelAdmin):

    list_display = ('appid', 'pkgname', 'isapk')

admin.site.register(Applist, ApplistAdmin)


class AppAdmin(admin.ModelAdmin):

    list_display = ('appid', 'name', 'pkgname', 'fileSize', 'price', 'numDownloads', 'ratingValue')

admin.site.register(App, AppAdmin)


class CommentsAdmin(admin.ModelAdmin):

    list_display = ('username', 'appid', 'comments', 'date')

admin.site.register(Comments, CommentsAdmin)
