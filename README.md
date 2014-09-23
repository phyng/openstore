Open Store
===========

## 简介
一个Django项目，开源的应用商店
目标是做Play Store数据存档

## 实现的功能
* 从Coolapk.com和Play Store抓取数据保存到MySQL
* 用户系统/用户评论系统/用户资料页面
* 图片代理和存储策略：因为Play Store被墙，第一次访问图片是通过 /store/proxy?url=https://*.ggpht.com/* 代理访问Google图片（即服务器先下载再返回），访问一次之后自动保存图片到 /static/img/*.png，第二次访问将会直接返回 /static/img/*.png
* Bootstrap 响应式前端

## 依赖
Django (1.7)
MySQL-python (1.2.5)
pathlib (1.0) #简洁强大的path库，Python 3开始内置
Pillow (2.3.0) #处理图像
requesocks (0.10.8) #支持socks5代理的requests
requests (2.2.1)

## 部署
参考 [http://phyng.com/2014/09/20/django-uwsgi-nginx/](http://phyng.com/2014/09/20/django-uwsgi-nginx/)

