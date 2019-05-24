from django.shortcuts import render, HttpResponse, redirect
from app01 import forms
from django.http import JsonResponse
from django.contrib import auth
from geetest import GeetestLib
from app01 import models
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# Create your views here.


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"

# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 滑动效验
def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)  # 将登录用户赋值给request.user
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login2.html")


def qq(request):
    pass


def weibo(request):
    pass


def weixin(request):
    pass


# @login_required
def index(request):
    # 查询所有文章列表
    # print(request.session.get('user_id'))
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


def logout(request):
    auth.logout(request)
    return redirect('/login/')


def upload(request):
    if request.method == "POST":
        filename = request.FILES.get('upload_file')
        # print(filename)
        with open(filename.name, 'wb') as f:
            for i in request.FILES['upload_file'].chunks():
                f.write(i)
    return render(request, 'upload.html')


def register(request):
    form_obj = forms.RegForm()
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        # 让form帮我们做校验
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            is_exist = models.UserInfo.objects.filter(username=username)
            if is_exist:
                # 拜师用户名已注册
                ret["status"] = 1
                ret["msg"] = "用户名已存在！"
                return JsonResponse(ret)
            # 效验通过，去数据库创建一个用户
            # del form_obj.cleaned_data["re_password"]
            form_obj.cleaned_data.pop('re_password')
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)

    return render(request, 'register.html', {"form_obj": form_obj})


# 专门效验用户名是否已被注册
def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册!"
    return JsonResponse(ret)


# 个人博客主页
def home(request, username):
    # print(username)
    # 去UserInfo表里把用户对象取出来
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    # 如果用户存在需要将TA写的所有对象取出来
    blog = user.blog

    # article_list
    article_list = models.Article.objects.filter(user=user)
    # 我的文章及每个分类下文章数
    # 将我的文章按照我的分类分组，并统计出每个分类下面的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # 统计当前站点下有哪些标签， 并且按标签统计出文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # 按日期归档
    archive_list = models.Article.objects.filter(user=user).values("create_time").annotate(c=Count("nid")).values("create_time", "c")
    return render(request, 'home.html', {
        'blog': blog,
        "user": user,
        "article_list": article_list,
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list,
    })


def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog

    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    archive_list = models.Article.objects.filter(user=user).annotate(c=Count("nid")).values("create_time", "c")
    # print(archive_list, '==========')
    # print(category_list)
    return archive_list, tag_list, category_list


def article_detail(request, username, pk):
    """
    :param username: 被访问的blog的用户名
    :param request:
    :param pk: 访问的文章的主键id值
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    archive_list, tag_list, category_list = get_left_menu(username)
    comment_list = models.Comment.objects.filter(article_id=pk)
    # print("="*80)
    return render(
        request, "article_detail.html", {
            "article": article_obj,
            "blog": blog,
            "user": user,
            "category_list": category_list,
            "tag_list": tag_list,
            "archive_list": archive_list,
            "comment_list": comment_list,
        }
    )


from django.db.models import F
def up_down(request):
    # print(request.POST)
    article_id = request.POST.get('article_id')
    is_up = json.loads(request.POST.get('is_up'))
    user = request.user
    response = {"state": True}
    # print('is_up', is_up)
    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
    except Exception as e:
        response['state'] = False
        response["first_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
    return JsonResponse(response)


def comment(request):
    # print(request.POST)
    pid = request.POST.get("pid")
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    user_pk = request.user.pk
    response = {}
    if not pid:  # 根评论
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content)
    else:  # 子评论
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content, parent_comment_id=pid)
    response['create_time'] = comment_obj.create_time.strftime("%Y-%m-%d")
    response['content'] = comment_obj.content
    response['username'] = comment_obj.user.username
    # print("="*80)
    # print(response)

    return JsonResponse(response)


def comment_tree(request, article_id):

    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment_id"))
    # print(ret)

    return JsonResponse(ret, safe=False)  # 如果不是字典要进行序列化就要加safe=False


@login_required
def add_article(request):
    if request.method == "POST":
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        user = request.user
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, "html.parser")
        desc = bs.text[0:150] + "..."
        # 过滤非法标签
        for tag in bs.find_all():
            if tag.name in ['script', 'link']:
                tag.decompose()
        article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        return redirect("/index/")
    return render(request, 'add_article.html')


from Django3 import settings
import os, json
def new_upload(request):
    # print(request.FILES)
    obj = request.FILES.get("imgFile")
    path = os.path.join(settings.MEDIA_ROOT, obj.name)
    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    ret = {
        "error": 0,
        "url": "/media/"+obj.name
    }

    return HttpResponse(json.dumps(ret))


def itemize(request):
    user = request.GET.get('user')
    message = request.GET.get('message', None)
    time = request.GET.get('time', None)
    username = models.UserInfo.objects.filter(username=user).first()
    if not username:
        return HttpResponse("404")
    if time:
        datetime = time.split("-")
        article_list = models.Article.objects.filter(user=username, create_time__year=datetime[0], create_time__month=datetime[1], create_time__day=datetime[2])

    if message:
        category = models.Category.objects.filter(title=message).first()
        article_list = models.Article.objects.filter(category=category, user=username)

    archive_list, tag_list, category_list = get_left_menu(username)
    return render(request, 'gatetory.html',
                  {
                      "article_list": article_list,
                      "archive_list": archive_list,
                      "tag_list": tag_list,
                      "category_list": category_list

                  })



# # ORM多列查询  返回QuerySet字典
# ret = models.Category.objects.all().values('nid', 'title', 'blog')
# print(ret)
# # ORM多列查询 返回QuerySet列表
# ret = models.UserInfo.objects.all().values_list('nid', 'phone')
# print(ret)
# # ORM多表查询
# ret = models.UserInfo.objects.all().select_related('blog')
# for i in ret:
#     print(i)