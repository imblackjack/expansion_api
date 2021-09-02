from django.db import models


class Projects(models.Model):
    app_name = models.CharField(default='', max_length=32, verbose_name='应用名')
    did = models.IntegerField(default=0, verbose_name='dtree_id')
    ip = models.CharField(default='', max_length=1024, verbose_name='部署IP')

    source = models.CharField(default='', max_length=32, null=True, blank=True, verbose_name='源服务器IP')
    s_port = models.IntegerField(default=22, max_length=32, null=True, blank=True, verbose_name='源ssh_port')
    s_code = models.CharField(default='', max_length=1024, null=True, blank=True, verbose_name='源代码path')
    code_status = models.IntegerField(default=0, max_length=32, null=True, blank=True, verbose_name='下载代码状态')


    status = models.BooleanField(default=False, db_column='status')
    # dtree_info = models.CharField(default='', max_length=1024, null=True, blank=True, verbose_name='dtree信息')
    paas_name = models.CharField(default='', max_length=32, null=True, blank=True, verbose_name='服务器名')

    class Meta:
        verbose_name = '应用管理'
        verbose_name_plural = verbose_name


'''
class Test(models.Model):
    # name varchar(32) not null default ''
    name = models.CharField(max_length=32, db_column='appname', null=False, default='')
    # create_time
    create_time = models.DateTimeField(null=False)
'''