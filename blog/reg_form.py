from django import forms
from django.forms import widgets
import re
from django.core.exceptions import ValidationError
from blog import models


# 自定义验证规则
def phone_num_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[0-9]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号格式错误')


# 定义一个注册的form类
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        widget=widgets.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入用户名"}
        ),
        error_messages={
            "max_length": "用户名最长16位",
            "required": "用户名不能为空",
        },
    )
    pwd = forms.CharField(
        min_length=6,
        max_length=20,
        label="密码",
        widget=widgets.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请输入密码"},
            render_value=True,
        ),
        error_messages={
            "min_length": "密码最少6位",
            "max_length": "密码最多20位",
            "required": "密码不能为空",
        },
    )
    re_pwd = forms.CharField(
        min_length=6,
        max_length=20,
        label="密码",
        widget=widgets.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请再次输入密码"},
            render_value=True,
        ),
        error_messages={
            "min_length": "密码最少6位",
            "max_length": "密码最多20位",
            "required": "密码不能为空",
        },
    )
    email = forms.EmailField(
        max_length=30,
        label="邮箱",
        widget=widgets.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入邮箱"}
        ),
        error_messages={
            "invalid": "邮箱格式不正确",
            "max_length": "邮箱最多30位",
            "required": "邮箱不能为空",
        },
    )
    phone_num = forms.CharField(
        label="手机号",
        widget=widgets.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入手机号"}
        ),
        error_messages={
            "required": "手机号不能为空"
        },
        validators=[phone_num_validate, ],
    )
