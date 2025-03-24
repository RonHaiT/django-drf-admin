import os
import django

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drfadmin.settings.local")
django.setup()

from user.models import Menu

def add_menu_data():
    # 预设菜单数据
    menu_list = [
        {'name': '系统设置', 'icon': 'bx-cog', 'sort': 1, 'enable': 1, 'type': 1, 'parent': None},
        {'name': '博客管理', 'icon': 'bxl-blogger', 'sort': 2, 'enable': 1, 'type': 1, 'parent': None},
    ]

    submenu_list = [
        {'name': '菜单管理', 'icon': 'bx-menu', 'sort': 1, 'url': '/system/Menu', 'enable': 1, 'type': 2, 'parent': '系统设置'},
        {'name': '角色管理', 'icon': 'bx-user', 'sort': 2, 'url': '/system/Role', 'enable': 1, 'type': 2, 'parent': '系统设置'},
        {'name': '用户管理', 'icon': 'bxs-user-detail', 'sort': 3, 'url': '/system/User', 'enable': 1, 'type': 2, 'parent': '系统设置'},
        {'name': '标签管理', 'icon': 'bx-crown', 'sort': 1, 'url': '/blog/Tag', 'enable': 1, 'type': 2, 'parent': '博客管理'},
        {'name': '分类管理', 'icon': 'bx-category', 'sort': 2, 'url': '/blog/Category', 'enable': 1, 'type': 2, 'parent': '博客管理'},
    ]

    button_list = [
        {'name': '添加菜单', 'icon': 'bx-plus', 'sort': 1, 'enable': 1, 'type': 3, 'parent': '菜单管理'},
        {'name': '编辑菜单', 'icon': 'bx-edit', 'sort': 2, 'enable': 1, 'type': 3, 'parent': '菜单管理'},
        {'name': '删除菜单', 'icon': 'bx-trash', 'sort': 3, 'enable': 1, 'type': 3, 'parent': '菜单管理'},
        {'name': '添加角色', 'icon': 'bx-plus', 'sort': 1, 'enable': 1, 'type': 3, 'parent': '角色管理'},
        {'name': '编辑角色', 'icon': 'bx-edit', 'sort': 2, 'enable': 1, 'type': 3, 'parent': '角色管理'},
        {'name': '删除角色', 'icon': 'bx-trash', 'sort': 3, 'enable': 1, 'type': 3, 'parent': '角色管理'},
    ]

    # 先创建顶级菜单
    created_menus = {}
    for menu_data in menu_list:
        menu = Menu.objects.create(**menu_data)
        created_menus[menu_data['name']] = menu  # 存储菜单对象

    # 创建子菜单
    for submenu_data in submenu_list:
        parent_menu = created_menus.get(submenu_data['parent'])
        if parent_menu:
            submenu_data['parent'] = parent_menu
            submenu = Menu.objects.create(**submenu_data)
            created_menus[submenu_data['name']] = submenu

    # 创建按钮
    for button_data in button_list:
        parent_menu = created_menus.get(button_data['parent'])
        if parent_menu:
            button_data['parent'] = parent_menu
            Menu.objects.create(**button_data)

    print("菜单数据成功添加到数据库！")

if __name__ == '__main__':
    add_menu_data()
