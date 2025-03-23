#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 晚生隆海
import requests
from lxml import etree
import re
import json

# 1.拿到boxicons的页面
url = 'https://boxicons.com/'
headers = {
    "Referer": "https://boxicons.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码是否为200
if response.status_code == 200:
    # 将响应内容保存到文件
    with open('boxicons_page.html', 'w',encoding='utf-8') as f:
        f.write(response.text)
    print("网页内容已保存到boxicons_page.html")
else:
    print("无法获取网页内容，状态码:", response.status_code)

## 2.解析找到所有的类名
tree = etree.parse('boxicons_page.html')
icons = tree.xpath(
    '//div[@class="IconMap_icongrid__asXvj"]/div[@class="Icon_icon_container__NTwhP   "]/div[@class="Icon_icon_select__tLN6i"]/div[1]/i')
icon_list = []
# 3.组装类名为list
for index, icon in enumerate(icons, start=1):
    icon_class = icon.get('class')
    match = re.search(r'bx\s+(.+)', icon_class)
    if match:
        content_after_bx = match.group(1)
        print(content_after_bx)
        # 截取类名中的图标类型
        icon_type = 1  # Regular
        if content_after_bx.startswith('bxs'):
            icon_type = 2  # 线性图标Solid
        elif content_after_bx.startswith('bxl'):
            icon_type = 3  # Logo

        icon_data = {"id": index, "boxicons": content_after_bx, "type": icon_type}
        icon_list.append(icon_data)

# 4.将对象列表转换为JSON格式,保存为js文件
json_data = json.dumps(icon_list, indent=4)
with open('boxicons.js', 'w') as f:
    f.write(f'var icons = {json_data};')
