Open Store
===========

## 简介
开源的应用商店， Django 项目，目标是做 Play Store 数据存档

Demo: [https://open.phyng.com/store/](https://open.phyng.com/store/)

## 已经实现的功能
* 爬虫，从 Play Store 抓取数据保存到 MySQL
* 用户系统
* 评论系统
* 使用七牛 API 存取图片
* 全站 SSL 访问
* Bootstrap 响应式前端

## 策略
* 主数据库使用 MySQL ，高频键值数据使用 Redis 
* 图片代理和存储策略：爬虫仅抓取图片 URL，因为 Play Store 被墙，第一次访问图片是通过`/store/proxy?url=`代理下载图片上传到七牛，然后302重定向到七牛图片地址，第二次及以后直接访问七牛，如果某个 URL 从未被访问，那么将不会下载图片

## 依赖
* Django (1.7)
* MySQL-python (1.2.5) 
* redis (2.10.3)
* pathlib (1.0)
* Pillow (2.3.0) 
* requesocks (0.10.8)
* requests (2.2.1)

## 部署
参考 [http://phyng.com/2014/09/20/django-uwsgi-nginx/](http://phyng.com/2014/09/20/django-uwsgi-nginx/)

