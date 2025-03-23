import os
import django

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_drf.settings")
django.setup()
# 必须放在setup后
from user.models import Role


def add_role_data():
    # 添加数据逻辑
    role_list = [
        {
            'name': '超级管理员',
            'desc': '超级用户'
        },
        {
            'name': '管理员',
            'desc': '管理员'
        }
    ]
    role_instances = [Role(**role_data) for role_data in role_list]
    try:
        Role.objects.bulk_create(role_instances)
    except Exception as e:
        print("角色数据成功添加到数据库。")
        print(f"Error: {e}")


if __name__ == '__main__':
    add_role_data()
