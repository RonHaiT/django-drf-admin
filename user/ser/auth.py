#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
from rest_framework import serializers
from user import models
from user.ser.role import RoleSerializers


class UserListSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    roles = RoleSerializers(many=True)

    class Meta:
        model = models.UserInfo
        fields = ['id', 'username', 'nickname', 'password', 'confirm_password', 'email', 'avatar', 'mobile', 'qq', 'wx',
                  'weibo',
                  'roles', 'create_time',
                  'update_time']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class AuthSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Role.objects.all(), required=False)

    class Meta:
        model = models.UserInfo
        fields = ['id', 'username', 'nickname', 'password', 'confirm_password', 'email', 'avatar', 'mobile', 'qq', 'wx',
                  'weibo',
                  'roles', 'create_time',
                  'update_time']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        print('validated_data', validated_data)
        confirm_password = validated_data.pop('confirm_password', None)
        roles_data = validated_data.pop('roles', [])  # Extract roles data from validated_data
        user = models.UserInfo.objects.create(**validated_data)  # Create user instance
        user.roles.set(roles_data)
        # Now, add roles to the created user
        # for role_id in roles_data:
        #     role = models.Role.objects.get(id=role_id)
        #     user.roles.add(role)

        return user


class AuthDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Role.objects.all(), required=False)

    class Meta:
        model = models.UserInfo
        fields = ['id', 'username', 'nickname', 'email', 'avatar', 'mobile', 'qq', 'wx',
                  'weibo',
                  'roles', 'create_time',
                  'update_time']
        extra_kwargs = {
            'password': {'write_only': True},
        }
