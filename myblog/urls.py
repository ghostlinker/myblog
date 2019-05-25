from django.conf.urls import url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^index/$', views.index),
    url(r'^reg/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    # 所有的api
    url(r'^api/check_user/$', views.check_user),
]
