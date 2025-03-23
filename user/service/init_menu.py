import os
import django

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_drf.settings")
django.setup()

from user.models import Menu


def add_menu_data():
    # 添加数据逻辑
    menu_list = [
        {
            'name': '系统设置', 'boxicons': 'bx-cog', 'sort': 1, 'enable': 1, 'type': 1, 'parent': 0
        },
        {
            'name': '菜单管理', 'boxicons': 'bx-menu', 'sort': 1, 'url': '/system/Menu', 'enable': 1, 'type': 2,
        },
        {
            'name': '添加菜单', 'boxicons': 'bx-menu', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '编辑菜单', 'boxicons': 'bx-menu', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '删除菜单', 'boxicons': 'bx-menu', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '角色管理', 'boxicons': 'bx-user', 'sort': 1, 'url': '/system/Role/', 'enable': 1, 'type': 2,

        },
        {
            'name': '添加角色', 'boxicons': 'bx-user', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,

        },
        {
            'name': '编辑角色', 'boxicons': 'bx-user', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,

        },
        {
            'name': '删除角色', 'boxicons': 'bx-user', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,

        },
        {
            'name': '用户管理', 'boxicons': 'bxs-user-detail', 'sort': 1, 'url': '/system/User', 'enable': 1, 'type': 2,
        },
        {
            'name': '添加用户', 'boxicons': 'bxs-user-detail', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '编辑用户', 'boxicons': 'bxs-user-detail', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '删除用户', 'boxicons': 'bxs-user-detail', 'sort': 1, 'url': '', 'enable': 1, 'type': 3,
        },
        {
            'name': '博客管理', 'boxicons': 'bxl-blogger', 'sort': 1, 'url': '', 'enable': 1, 'type': 1,
        },
        {
            'name': '标签管理', 'boxicons': 'bx-crown', 'sort': 1, 'url': '/blog/Tag', 'enable': 1, 'type': 2,
        },
        {
            'name': '分类管理', 'boxicons': 'bx bx-category', 'sort': 1, 'url': '/blog/Category', 'enable': 1, 'type': 2,
        },
    ]
    menu_instances = [Menu(**menu_data) for menu_data in menu_list]
    try:
        Menu.objects.bulk_create(menu_instances)
        print("菜单数据成功添加到数据库。")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    add_menu_data()
