"""Django3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings
from app01 import urls as blog_url
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^upload/', views.upload),
    url(r'^new_upload/', views.new_upload),
    url(r'^reg/', views.register),
    url(r'^login/qq', views.qq),
    url(r'^login/weibo/', views.weibo),
    url(r'^login/weixin', views.weixin),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^pc-geetest/register', views.get_geetest),
    # 专门效验用户名是否一样的url
    url(r'^check_username_exist/$', views.check_username_exist),
    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 将所有以blog开头的url都交给app下面的urls.py来处理
    url(r'^blog/', include(blog_url)),
]
