from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog import models, reg_form
from django.db.models import Count
from django.contrib import auth


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')[:10]
    category_list = models.Category.objects.annotate(c=Count("article")).values("title", "c").all()
    tag_list = models.Tag.objects.annotate(c=Count("article")).values("title", "c").all()
    archive_list = models.Article.objects.all().extra(
        select={"archive_ym": "date_format(create_time, '%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("article_id")).values("archive_ym", "c")
    return render(request, "index.html", {"article_list": article_list,
                                          "category_list": category_list,
                                          "tag_list": tag_list,
                                          "archive_list": archive_list,
                                          })


def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册
    #     return redirect("/index/")
    #
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        register_form = reg_form.RegForm(request.POST)
        if register_form.is_valid():
            register_form.cleaned_data.pop("re_pwd")
            models.UserInfo.objects.create_user(**register_form.cleaned_data)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = register_form.errors
            print(register_form.errors)
            return JsonResponse(ret)
    reg_obj = reg_form.RegForm()
    return render(request, 'register.html', {"reg_obj": reg_obj})


def check_user(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册！"
    return JsonResponse(ret)


def login(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 利用auth模块对用户和密码做校验
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            ret["msg"] = "/index/"
        else:
            # 用户名或密码错误，给出提示
            ret["status"] = 1
            ret["msg"] = "用户名或密码错误！"
        return JsonResponse(ret)
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("/index/")
