from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.utils.auth import CustomTokenObtainPairSerializer
from user import models
from user.utils import code
from user.utils.menu import process_menu
from user.ser.menu import MenuSerializers
from rest_framework.views import APIView
from user.ser.auth import UserListSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.ser.auth import AuthSerializer, AuthDetailSerializer
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError


class MyLoginView(TokenObtainPairView):
    """
    登录视图，继承自 TokenObtainPairView
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            # 执行登录逻辑
            res_data = super().post(request, *args, **kwargs)
            # 获取菜单信息
            queryset = models.Menu.objects.all()
            ser = MenuSerializers(instance=queryset, many=True)
            # 组装菜单列表
            menu_tree = process_menu(ser.data)
            # token过期时间
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            # 刷新token过期时间
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            # 将有效期转换为秒数
            expire = access_token_lifetime.total_seconds()
            refresh_expires_in = refresh_token_lifetime.total_seconds()
            # 构造响应数据
            response_data = {
                'token': res_data.data.pop('access', None),
                'refresh': res_data.data.pop('refresh', None),
                'username': request.user.username,
                'expire': int(expire),
                'menulist': menu_tree,
            }
            return Response({'status': code.HTTP_SUCCESS, 'msg': code.HTTP_SUCCESS_MSG, 'data': response_data})
        except AuthenticationFailed as e:
            # 如果验证失败，则捕获异常并返回相应的错误消息
            return Response({'code': code.HTTP_AUTHENTICATION_FAILED, 'msg': str(e)})


class MyRefreshView(TokenRefreshView):
    """刷新token"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': str(e), 'status': code.HTTP_EXPIRE}, )
        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh = serializer.validated_data.get('refresh')

        # 创建新的刷新 token
        refresh_token = RefreshToken(refresh)

        # 使用新的刷新 token 创建新的访问 token
        access_token = refresh_token.access_token
        expire = access_token_lifetime.total_seconds()
        # 返回新的访问 token 和刷新 token
        return Response({
            'token': str(access_token),
            'refresh': str(refresh_token),
            'expire': int(expire),
        })


class UserView(APIView):

    def get(self, request):
        queryset = models.UserInfo.objects.all()
        ser = UserListSerializers(instance=queryset, many=True)
        return Response({'status': 0, 'msg': '成功', 'data': ser.data})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': '认证失败'}, status=code.HTTP_AUTHENTICATION_FAILED)

        ser = AuthSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)
            return Response({'status': 0, 'msg': '成功', 'data': ser.data})
        else:
            return Response({'status': code.HTTP_AUTHENTICATION_FAILED, 'msg': ser.errors})


class UserDetailView(APIView):
    def get(self, request, pk):
        user_object = models.UserInfo.objects.filter(pk=pk).first()
        serializer = AuthDetailSerializer(instance=user_object)
        result = {'status': code.HTTP_SUCCESS, 'msg': '修改成功', 'data': serializer.data}
        return Response(result)

    def put(self, request, pk):
        user_object = models.UserInfo.objects.filter(pk=pk).first()
        if not user_object:
            result = {'status': code.HTTP_NOT_FOUND, 'msg': '数据不存在', }
            return Response(result)
        serializer = AuthDetailSerializer(user_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = {'status': code.HTTP_SUCCESS, 'msg': '修改成功', 'data': serializer.data}
            return Response(result)

        result = {'status': code.HTTP_ERROR, 'msg': serializer.errors}
        return Response(result)

    def delete(self, request, pk):
        try:
            user = models.UserInfo.objects.get(id=pk)
        except models.UserInfo.DoesNotExist:
            result = {'status': code.HTTP_SUCCESS, 'msg': '数据不存在'}
            return Response(result)
        user.delete()
        result = {'status': code.HTTP_SUCCESS, 'msg': "删除成功"}
        return Response(result)
