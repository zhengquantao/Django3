from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app01 import models


# 定义一个注册的form类
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        widget=forms.widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "max_length": "用户名最长16位",
            "required": "密码不能为空",
        }
    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码最少6位",
            "required": "密码不能为空"
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码最少6位",
            "required": "密码不能为空"
        }
    )
    phone = forms.CharField(
        label="手机",
        validators=[
            RegexValidator(r'^1[3-9][0-9]{9}$', '手机格式不正确')
        ],
        widget=forms.widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "手机不能为空"
        }
    )
    email = forms.EmailField(
        label="邮箱",
        widget=forms.widgets.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "invalid": "邮箱格式不正确",
            "required": "邮箱不能为空"
        }
    )

    # 重写username字段的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            # 表示用户名已注册
            self.add_error("username", ValidationError("用户名已存在！"))
        else:
            return username

        # 重写email字段的局部钩子
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            # 表示邮箱名已注册
            self.add_error("email", ValidationError("邮箱名已存在！"))
        else:
            return email

    # 重写全局的钩子函数， 对确认密码做效验
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致"))
        else:
            return self.cleaned_data
