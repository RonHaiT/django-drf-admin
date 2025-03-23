#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
from rest_framework import serializers
from user import models


class RoleSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    menus = serializers.SerializerMethodField()

    class Meta:
        model = models.Role
        fields = ['id', 'name', 'create_time', 'update_time', 'desc', 'menus']

    def get_menus(self, obj):
        menus = obj.menus.all() if obj.menus else []  # 获取角色对象关联的所有菜单对象，如果为空则返回空列表
        menu_ids = [menu.id for menu in menus]  # 提取菜单对象的ID
        return menu_ids
