from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用 MySQL
        'NAME': 'blog',  # 数据库名称
        'USER': 'root',  # MySQL 用户
        'PASSWORD': 'root123456',  # MySQL 密码
        'HOST': 'localhost',  # 数据库服务器地址，远程则改为 IP 地址
        'PORT': '3306',  # MySQL 端口，默认 3306
        'OPTIONS': {
            'charset': 'utf8mb4',  # 推荐使用 utf8mb4 支持 Emoji
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # 避免非严格模式带来的数据问题
        },
    }
}