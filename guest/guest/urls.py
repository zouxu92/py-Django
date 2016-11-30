# -*- coding:utf-8 -*-
"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sign import views
# 导入sign应用views文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index), # 添加 index/路径配置
    url(r'^login_action/$', views.login_action),
    url(r'^event_manage/$', views.event_manage), # 添加登录后的跳转
    url(r'^accounts/login/$', views.index),
    url(r'^sreach_name/$', views.sreach_name),  # 发布会名称搜索
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^sreach_phone/$', views.sreach_phone), # 嘉宾姓名搜索
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index), # 签到页面
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action), # 签到动作
]
