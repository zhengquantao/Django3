import os


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django3.settings")
    import django
    django.setup()

    from app01 import models
    # ORM分组查询 每个部门名称及部门的平均工资
    ret = models.Employee.objects.all()
    '''
    SELECT "employee"."id", "employee"."name", "employee"."age", "employee"."salary",\
     "employee"."province", "employee"."dept" FROM "employee" LIMIT 21; args=()
     '''
    ret = models.Employee.objects.all().values('dept', 'age')
    '''
    SELECT "employee"."dept", "employee"."age" FROM "employee" LIMIT 21; args=()
    '''
    from django.db.models import Avg
    ret = models.Employee.objects.values('dept').annotate(a=Avg('salary')).values('dept', 'a')
    '''
    SELECT "employee"."dept", AVG("employee"."salary") AS "a" FROM "employee" GROUP BY "employee"."dept" LIMIT 21;\
     args=()
    '''
    # ORM连表分组查询
    ret = models.People.objects.values("dept_id").annotate(a=Avg("salary")).values("dept__name", "a")
    """
    SELECT "dept"."name", AVG("people"."salary") AS "a" FROM "people" INNER JOIN "dept" ON ("people"."dept_id" = "dept".
    "id") GROUP BY "people"."dept_id", "dept"."name" LIMIT 21; args=()
    """
    # 查询people表，判断每个人的工资是否大于2000
    ret = models.People.objects.all().extra(
        select={"gt": "salary > 2000"}
    )
    """
    SELECT (salary > 2000) AS "gt", "people"."id", "people"."name", "people"."salary", "people"."dept_id" FROM "people"\
     LIMIT 21; args=()
     """
    # 执行原声的SQL语句
    from django.db import connection
    cursor = connection.cursor()  # 获取光标，等待实行SQL语句
    cursor.execute("""SELECT * from people where id = %s""", [1])
    ret = cursor.fetchone()
    """
    SELECT * from people where id = 1; args=[1]
    """
    from django.db.models import Count
    user = models.UserInfo.objects.filter(username='taozhengquan').first()
    blog = user.blog
    ret = models.Category.objects.filter(blog=blog)  # 求小黑站点下面所有文章分类
    # ret = ret[0].article_set.all()
    # ret.annotate(a=Count("article"))
    for i in ret:
        print(i.title, i.article_set.all().count())
    ret = models.Article.objects.filter(user=user).extra(   # mysql时间格式化为date_format()
        select={"archive_ym": "datetime(create_time, '%%Y%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
    print(ret)
