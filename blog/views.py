from django.shortcuts import render
from blog import models, reg_form


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')[:10]
    return render(request, "index.html", {"article_list": article_list})


def register(request):
    reg_obj = reg_form.RegForm()
    return render(request, 'register.html', {"reg_obj": reg_obj})
