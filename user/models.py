from django.db import models
from django.contrib.auth.models import AbstractUser


class Menu(models.Model):
    """
    菜单表
    """
    enabled_choices = ((0, '隐藏'), (1, '显示'))
    permission_choices = (('add', '添加'), ('edit', '编辑'), ('del', '删除'))
    type_choices = ((1, '目录'), (2, '页面'), (3, '按钮'))

    name = models.CharField(verbose_name='菜单名称', max_length=32, unique=True)
    icon = models.CharField(verbose_name='菜单图标', max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='所属父级菜单ID', null=True, blank=True,
                               help_text='所属父级菜单,顶级为0')
    sort = models.IntegerField(verbose_name='排序', help_text='排序号序号越大排序越靠前',blank=True, null=True)
    url = models.CharField(verbose_name='路由地址', max_length=200, blank=True, null=True)

    enable = models.IntegerField(verbose_name='是否启用', choices=enabled_choices)
    type = models.IntegerField(verbose_name='权限类型', choices=type_choices)
    btn_permission = models.CharField(verbose_name='按权限标识', max_length=8, choices=permission_choices, null=True,
                                      blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_menus'


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(verbose_name='角色名称', max_length=32,unique=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    menus = models.ManyToManyField(verbose_name='拥有的菜单', to='Menu', blank=True)
    desc = models.CharField(verbose_name='角色描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_roles'


class UserInfo(AbstractUser):
    """
    用户表
    """
    nickname = models.CharField(verbose_name='用户昵称', max_length=128)
    avatar = models.CharField(verbose_name='头像', max_length=256)
    mobile = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    qq = models.CharField(verbose_name='qq', max_length=32, blank=True, null=True)
    wx = models.CharField(verbose_name='微信', max_length=32, blank=True, null=True)
    weibo = models.CharField(verbose_name='微博', max_length=32, blank=True, null=True)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'sys_userinfo'
