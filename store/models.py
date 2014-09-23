# coding: utf-8
from django.db import models

import django


# Create your models here.

class Applist(models.Model):

    appid = models.IntegerField(unique=True, db_index=True)

    isapk = models.IntegerField(default=1)
    pkgname = models.CharField(max_length=100, default='None')

    def __unicode__(self):
        return self.pkgname

class App(models.Model):

    appid = models.IntegerField(unique=True, db_index=True)
    pkgname = models.CharField(max_length=100, default='None', unique=True)

    name = models.CharField(max_length=100, default='None')
    author = models.CharField(max_length=100, default='None')
    price = models.FloatField(default=0, db_index=True)
    icon = models.CharField(max_length=100)

    ratingValue = models.FloatField(default=0, db_index=True)
    ratingCount = models.IntegerField(default=0)
    rating5 = models.IntegerField(default=0)
    rating4 = models.IntegerField(default=0)
    rating3 = models.IntegerField(default=0)
    rating2 = models.IntegerField(default=0)
    rating1 = models.IntegerField(default=0)

    fileSize = models.CharField(max_length=50)
    numDownloads = models.CharField(max_length=50)
    softwareVersion = models.CharField(max_length=50)
    operatingSystems = models.CharField(max_length=50)
    contentRating = models.CharField(max_length=50)

    imgs = models.TextField(max_length=1000)
    descs = models.TextField(max_length=10000)
    whatsnew = models.TextField(max_length=10000)
    similar = models.TextField(max_length=1000)

    def get_img_list(self):
        return self.imgs.split(',')

    def get_similar(self):
        return self.similar.split(',')

    def get_rating(self):
        li = (self.rating5, self.rating4, self.rating3, self.rating2, self.rating1)
        return [str(float(i) / (float(sum(li)) + 0.000000001) * 100.0) for i in li]

    def get_rating_value(self):
        return int(self.ratingValue * 20)

    def get_num_download(self):
        try:
            return self.numDownloads.split('-')[0]
        except:
            return "None"

    def get_price(self):
        if int(self.price) == 0:
            return u"免费"
        else:
            return str(self.price) + u"美元"

    def __unicode__(self):
        return self.name

class Comments(models.Model):
    username = models.CharField(max_length=30, db_index=True)
    appid = models.IntegerField(db_index=True)
    comments = models.TextField(max_length=500)
    date = models.DateTimeField()

class Imglist(models.Model):
    appid = models.IntegerField(db_index=True)
    icon = models.CharField(max_length=10)
    other = models.CharField(max_length=100)
