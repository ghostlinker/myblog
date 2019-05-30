from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from blog import models, reg_form
from django.db.models import Count
from django.contrib import auth


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')[:20]
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


def home(request, username):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    article_list = models.Article.objects.filter(user=user).order_by('-create_time')[:20]
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c").all()
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c").all()
    archive_list = models.Article.objects.filter(user=user).all().extra(
        select={"archive_ym": "date_format(create_time, '%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("article_id")).values("archive_ym", "c")
    return render(request, "home.html", {
        "blog": blog,
        "article_list": article_list,
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list,
    })


def article_detail(request, username, pk):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    category_list = models.Category.objects.annotate(c=Count("article")).values("title", "c").all()
    tag_list = models.Tag.objects.annotate(c=Count("article")).values("title", "c").all()
    archive_list = models.Article.objects.all().extra(
        select={"archive_ym": "date_format(create_time, '%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("article_id")).values("archive_ym", "c")
    comment_list = models.Comment.objects.filter(article_id=pk)
    return render(request, "article_detail.html", {
        "article": article_obj,
        "blog": blog,
        "username": username,
        "comment_list": comment_list,
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list,
    })


def comment(request):
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    user_pk = request.user.pk
    pid = request.POST.get("pid")
    response = {}
    if not pid:
        # 没有pid，该评论为根评论，处理根评论
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content)
    else:
        # 有pid，该评论为子评论，处理子评论
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content,
                                                    parent_comment_id=pid)
    # 该文章的评论数量+1，这个逻辑后面补一下
    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d %H:%M")
    response["content"] = comment_obj.content
    response["username"] = comment_obj.user.username
    return JsonResponse(response)
