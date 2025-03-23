from django.urls import re_path, path
from user.views import user, menu, role

urlpatterns = [
    path('user/login/', user.MyLoginView.as_view()),
    path('user/refresh/', user.MyRefreshView.as_view()),

    path('menu/list/', menu.MenulistView.as_view()),
    re_path('menu/(?P<pk>\d+)/', menu.MenulistView.as_view(), name='delete_menu'),
    re_path('menu/update/', menu.MenulistView.as_view(), name='update_menu'),

    path('role/list/', role.RolelistView.as_view()),
    re_path('role/(?P<pk>\d+)/', role.RoleDetailView.as_view()),

    path('user/list/', user.UserView.as_view()),
    re_path('user/(?P<pk>\d+)/', user.UserDetailView.as_view(), name='delete_user'),
    re_path('user/(?P<pk>\d+)/', user.UserDetailView.as_view(), name='update_user'),
]
