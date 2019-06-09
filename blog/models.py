from django.db import models
from django.contrib.auth.models import AbstractUser
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# 扩展auth表
class UserInfo(AbstractUser):
    """
    用户信息表
    """
    user_id = models.AutoField(primary_key=True, verbose_name='用户id')
    phone_num = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    blog = models.OneToOneField(to="Blog", to_field="blog_id", null=True)  # 1对1关联博客信息表

    def __str__(self):
        return "用户id：%s，用户名：%s" % (self.user_id, self.username)

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """
    博客信息表
    """
    blog_id = models.AutoField(primary_key=True, verbose_name='博客id')
    title = models.CharField(max_length=128, verbose_name='个人博客标题')
    site = models.CharField(max_length=32, unique=True, verbose_name='个人博客后缀')

    def __str__(self):
        return "博客id：%s，博客标题：%s" % (self.blog_id, self.title)

    class Meta:
        db_table = "blog"
        verbose_name = "博客站点"
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    博客文章分类
    """
    category_id = models.AutoField(primary_key=True, verbose_name='文章分类id')
    title = models.CharField(max_length=32, verbose_name='分类标题')
    blog = models.ForeignKey(to="Blog", to_field="blog_id")  # 外键关联博客，一个站点可以有多个分类

    def __str__(self):
        return "分类id：%s，分类标题：%s" % (self.category_id, self.title)

    class Meta:
        db_table = "category"
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    """
    tag_id = models.AutoField(primary_key=True, verbose_name="标签id")
    title = models.CharField(max_length=32, verbose_name="标签名")
    blog = models.ForeignKey(to="Blog", to_field="blog_id")  # 所属博客

    def __str__(self):
        return "标签id：%s，标签名：%s" % (self.tag_id, self.title)

    class Meta:
        db_table = "tag"
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章
    """
    article_id = models.AutoField(primary_key=True, verbose_name="文章标题")
    title = models.CharField(max_length=50, verbose_name="文章标题")
    desc = models.CharField(max_length=255, verbose_name="文章描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    comment_count = models.IntegerField(default=0, verbose_name="评论数")
    up_count = models.IntegerField(default=0, verbose_name="点赞数")
    down_count = models.IntegerField(default=0, verbose_name="踩数")
    hit_count = models.IntegerField(default=0, verbose_name="点击数")
    category = models.ForeignKey(to="Category", to_field="category_id", null=True)  # 关联文章分类
    user = models.ForeignKey(to="UserInfo", to_field="user_id")  # 关联用户
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag"),
    )

    def __str__(self):
        return "文章id：%s，文章标题：%s" % (self.article_id, self.title)

    class Meta:
        db_table = "article"
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    detail_id = models.AutoField(primary_key=True, verbose_name="文章详情id")
    content = RichTextUploadingField(verbose_name="文章详情内容", config_name='default')
    article = models.OneToOneField(to="Article", to_field="article_id")  # 文章和文章详情一对一

    def __str__(self):
        return "详情id：%s，详情内容：%s" % (self.detail_id, self.content)

    class Meta:
        db_table = "articledetail"
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    文章与标签之间多对多的关系表
    """
    a2t_id = models.AutoField(primary_key=True, verbose_name="文章标签关系id")
    article = models.ForeignKey(to="Article", to_field="article_id")
    tag = models.ForeignKey(to="Tag", to_field="tag_id")

    class Meta:
        unique_together = (("article", "tag"),)
        db_table = "article2tag"
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    updown_id = models.AutoField(primary_key=True, verbose_name="点赞id")
    user = models.ForeignKey(to="UserInfo", null=True, verbose_name="点赞人")
    article = models.ForeignKey(to="Article", null=True, verbose_name="点赞文章")
    is_up = models.BooleanField(default=True, verbose_name="赞踩")  # 默认点赞

    class Meta:
        unique_together = (("article", "user"),)
        db_table = "articleupdown"
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    comment_id = models.AutoField(primary_key=True, verbose_name="评论id")
    article = models.ForeignKey(to="Article", to_field="article_id")
    user = models.ForeignKey(to="UserInfo", to_field="user_id")
    content = models.CharField(max_length=255, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    parent_comment = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return "评论id：%s，评论内容：%s" % (self.comment_id, self.content)

    class Meta:
        db_table = "comment"
        verbose_name = "评论"
        verbose_name_plural = verbose_name
