#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from user.models import UserInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.authentication import JWTAuthentication


class MyModelBackend(ModelBackend):
    """
    默认系统只校验用户名和密码，实际情况，可能有手机号，验证码等其他需要校验的
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            print(user)
            if user.check_password(password):
                # 将用户设置为请求的用户
                login(request, user)

                return user
            else:
                raise AuthenticationFailed('帐号或密码错误')
        except UserInfo.DoesNotExist:
            raise AuthenticationFailed('用户名或手机号未注册')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义的 验证邮箱和手机号用户名，用于在登录时向 JWT 中添加额外信息
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages['required'] = ('请输入用户名或手机号码或邮箱')
        self.fields['password'].error_messages['required'] = ('请输入密码')

    # def validate(self, attrs):
    #     print('validating')
    #     '''此方法是 响应数据结构，默认返回只有 access 和 refresh'''
    #     data = super().validate(attrs=attrs)
    #     # 获取Token对象
    #     refresh = self.get_token(self.user)
    #     data["refresh"] = str(refresh)
    #     data["token"] = str(refresh.access_token)
    #     # 令牌到期时间
    #     data['expire'] = refresh.access_token.payload['exp']  # 有效期
    #     # 用户名
    #     data['username'] = self.user.username
    #
    #     return data


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义的 认证类
    """
    def authenticate(self, request):
        # 调用父类的 authenticate 方法验证 JWT 令牌
        user = super().authenticate(request)

        # 如果验证失败，则抛出 AuthenticationFailed 异常
        if user is None:
            raise AuthenticationFailed('身份验证失败')

        # 如果验证成功，返回用户对象
        return user
