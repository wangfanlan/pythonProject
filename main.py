from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

# 指定要爬取的网址
url = 'https://photo.gmw.cn/2023-05/30/content_36593728.htm'
md_file_name = 'example.md'

# 发送 HTTP 请求获取网页内容
response = requests.get(url)

# 使用 BeautifulSoup 库解析 HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 创建保存图片的目录
img_dir = 'imgs'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

#创建计数器记录元素位置，初始值为0
count=0

# 找到所有图片链接，下载并插入到markdown文件中
for img in soup.find_all('img'):
    src = img.get('src')
    # 将相对路径转换为绝对路径
    if src and not src.startswith('http'):
        src = urljoin(url, src)

    # 下载并插入图片到markdown文件中
    if src:
        try:
            img_response = requests.get(src)
            img_content_type = img_response.headers.get('content-type')
            if 'image' not in img_content_type:
                continue

            img_name = re.split(r'[\\/:*?"<>|\r\n]+', src)[-1]
            with open(os.path.join(img_dir, img_name), 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded image: {img_name}")

            #插入图片到markdown文件中,并更新计数器的值
            with open(md_file_name,'a') as md_file:
                md_file.write(f"![{img['alt']}]({os.path.join(img_dir, img_name)})\n")
                count+=1

        except Exception as e:
            print(f"Failed downloading image: {src}")
            print(e)

    #获取文本内容
    for p in soup.find_all('p'):
        if p.text!=None:
            with open(md_file_name,'a') as md_file:
                #插入文本到markdown文件并更新计数器的值
                md_file.write(f"{p.text.strip()}\n")
                count+=1

        #处理版权信息和缺少宽度的图片
        for img in p.find_all('img'):
            width = img.attrs.get('width')
            if not width:
                #自动获取图片宽度和高度
                try:
                    img_response = requests.get(img['src'])
                    img_data = BytesIO(img_response.content)
                    with Image.open(img_data) as im:
                        img_width, _ = im.size
                        if img_width:
                            img['width'] = str(img_width) + 'px'

                            #在Markdown文件中插入图片，并更新计数器的值
                            with open(md_file_name,'a') as md_file:
                                md_file.write(f"![{img['alt']}]({img['src']})\n")
                                count+=1

                except Exception as e:
                    print(f"Failed when processing image: {img['src']}")
                    print(e)

#输出提示消息
print(f"Saved Markdown file: {md_file_name}") 