#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海

from rest_framework import serializers
from user import models


class MenuSerializers(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()

    class Meta:
        model = models.Menu
        fields = ['id', 'name', 'icon', 'parent', 'sort', 'url', 'path', 'type', 'enable', 'btn_permission']

    extra_kwargs = {
        'name': {'required': True, 'unique': False},
    }

    def create(self, validated_data):
        parent_id = self.initial_data.get('parent')
        if parent_id is not None:
            try:
                parent_instance = models.Menu.objects.get(pk=parent_id)
                validated_data['parent'] = parent_instance
            except models.Menu.DoesNotExist:
                # 处理父级菜单不存在的情况
                # 在这里您可以选择抛出异常、创建默认父级菜单或者采取其他适当的行动
                pass

        menu_instance = super().create(validated_data)
        return menu_instance

    def get_parent(self, obj):
        parent_data = obj.parent
        if parent_data:
            # 返回父级菜单的对象
            return MenuSerializers(parent_data).data
        return None

    def get_path(self, obj):
        if obj.url:
            path = ''.join(obj.url.split('/'))
            return path
        return None
