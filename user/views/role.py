#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
from rest_framework.views import APIView
from rest_framework.response import Response
from user.utils import code
from user import models
from user.ser.role import RoleSerializers
from django.utils import timezone
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet


class RolelistView(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializers

    def get(self, request):
        queryset = models.Role.objects.all()
        ser = RoleSerializers(instance=queryset, many=True)
        result = {'status': code.HTTP_SUCCESS, 'msg': code.HTTP_SUCCESS_MSG, 'data': ser.data}
        return Response(result)

    def post(self, request):
        # 检查用户是否已经登录
        if not request.user.is_authenticated:
            return Response({'error': '认证失败'}, status=code.HTTP_AUTHENTICATION_FAILED)
        # 获取菜单信息
        menu_ids = request.data.get('menus', [])
        menus = models.Menu.objects.filter(id__in=menu_ids)

        # 创建角色对象
        role_data = request.data.copy()
        role_data['menus'] = menus  # 将菜单信息添加到请求数据中
        ser = RoleSerializers(data=role_data)
        if ser.is_valid():
            role = ser.save()
            return Response({'status': 0, 'msg': '成功', 'data': ser.data})
        else:
            return Response({'status': code.HTTP_AUTHENTICATION_FAILED, 'msg': ser.errors})


class RoleDetailView(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializers

    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            # 找到要修改的数据对象
            pk = request.data.get('id', None)
            role_object = models.Role.objects.get(pk=pk)
        except models.Role.DoesNotExist:
            result = {'status': code.HTTP_NOT_FOUND, 'msg': '数据不存在', }
            return Response(result)
        # 检查是否有 menus 字段
        if 'menus' in request.data:
            menu_ids = request.data.get('menus', [])  # 获取菜单ID列表
            menus = models.Menu.objects.filter(id__in=menu_ids)  # 获取对应的菜单对象列表
            role_object.menus.set(menus)  # 设置角色对象的 menus 字段为获取到的菜单对象列表

        serializer = RoleSerializers(role_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = {'status': code.HTTP_SUCCESS, 'msg': '修改成功', 'data': serializer.data}
            return Response(result)

        result = {'status': code.HTTP_ERROR, 'msg': serializer.errors}
        return Response(result)

    def delete(self, request, pk):
        role = models.Role.objects.filter(id=pk).first()
        if not role:
            result = {'status': code.HTTP_SUCCESS, 'msg': '数据不存在'}
            return Response(result)
        role.delete()
        result = {'status': code.HTTP_SUCCESS, 'msg': "删除成功"}
        return Response(result)
