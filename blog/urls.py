from django.conf.urls import url
from blog import views

urlpatterns = [
    # 个人博客首页
    url(r'^(\w+)/$', views.home),
    # 文章详情
    url(r'^(\w+)/article/(\d+)/$', views.article_detail),
    # blog下所有的api
    url(r"^api/comment/$", views.comment),
    url(r"^api/up_down/$", views.up_down),
]
