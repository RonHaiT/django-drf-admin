#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海

def process_menu(menu_list):
    menu_dict = {}  # 使用字典以便按id查找菜单项
    menu_tree = []  # 用于存储树状结构的菜单项
    # 将所有菜单项按id存储到字典中
    for menu in menu_list:
        menu_dict[menu['id']] = menu

        # 将菜单项添加到相应的父菜单的children列表中
    for menu in menu_list:
        parent = menu['parent']
        if parent is not None:
            parent_id = parent.get('id')
            if parent_id is not None:
                parent_menu = menu_dict.get(parent_id)
                if parent_menu:
                    children_list = parent_menu.setdefault('children', [])
                    children_list.append(menu)
        else:
            # 一级菜单
            menu_tree.append(menu)
    for menu in menu_list:
        if 'children' not in menu:
            menu['children'] = None

    return menu_tree
