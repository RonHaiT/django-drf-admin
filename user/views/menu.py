#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
from rest_framework.views import APIView
from rest_framework.response import Response
from user import models
from user.ser.menu import MenuSerializers
from user.utils import code,menu
from django.utils import timezone

from rest_framework import status

class MenulistView(APIView):
    def get(self, request):
        queryset = models.Menu.objects.all()
        ser = MenuSerializers(instance=queryset, many=True)
        # 使用process_menu_data函数处理数据
        processed_data = menu.process_menu(ser.data)
        result = {'status': code.HTTP_SUCCESS, 'msg': code.HTTP_SUCCESS_MSG, 'data': processed_data}
        return Response(result)

    def post(self, request):
        # 从请求中获取数据
        data = request.data
        # 使用序列化器进行验证和处理数据
        serializer = MenuSerializers(data=data)
        if serializer.is_valid():
            # 如果数据验证通过，则创建菜单项
            serializer.save()
            # 返回成功响应
            result = {'status': code.HTTP_SUCCESS, 'msg': code.HTTP_SUCCESS_MSG, 'data': serializer.data}
            return Response(result)
        else:
            # 如果数据验证不通过，则返回错误响应
            errors = serializer.errors
            result = {'status': code.HTTP_BAD_REQUEST, 'msg': errors}
            return Response(result)

    def put(self, request):
        try:
            # 找到要修改的数据对象
            pk = request.data.get('id', None)
            menu_object = models.Menu.objects.get(pk=pk)
        except models.Menu.DoesNotExist:
            result = {'status': code.HTTP_NOT_FOUND, 'msg': '未找到该菜单', }
            return Response(result)
        request.data.pop('id', None)
        request.data['update_time'] = timezone.now()
        serializer = MenuSerializers(menu_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = {'status': code.HTTP_SUCCESS, 'msg': '菜单修改成功', 'data': serializer.data}
            return Response(result)

        result = {'status': code.HTTP_ERROR, 'msg': serializer.errors}
        return Response(result)

    def delete(self, request, pk):
        try:
            menu = models.Menu.objects.get(id=pk)
        except models.Menu.DoesNotExist:
            result = {'status': code.HTTP_SUCCESS, 'msg': '菜单不存在'}
            return Response(result)
        menu.delete()
        result = {'status': code.HTTP_SUCCESS, 'msg': "菜单删除成功"}
        return Response(result)
