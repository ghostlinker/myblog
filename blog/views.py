from django.shortcuts import render, redirect
from django.http import JsonResponse
from blog import models, reg_form


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')[:10]
    return render(request, "index.html", {"article_list": article_list})


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
