from django.shortcuts import render
from blog import models


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')[:10]
    return render(request, "index.html", {"article_list": article_list})
