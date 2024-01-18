import jieba
import numpy as np
from pathlib import Path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt


def split_four_text(text):
    # split_four_text函数用于jieba分词并分隔为4个字为一组的内容。

    words = jieba.cut(text)

    # 用Counter方法计算单词频率数
    count = Counter(words)
    most_count = count.most_common()
    words_list = []

    for i in most_count:
        if len(i[0]) == 4:
            words_list.append(i[0])

    return words_list


def draw_wordcloud(text, image_mask, ):
    # draw_wordcloud函数以用户定义的模板轮廓图来显示中文词云。

    sanguo_mask = np.array(Image.open(image_mask))

    wordcloud = WordCloud(background_color='white', mask=sanguo_mask,
                          max_words=1000,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path='/System/Library/Fonts/STHeiti Light.ttc')

    wordcloud.generate(text)

    image_colors = ImageColorGenerator(sanguo_mask)

    plt.figure(figsize=(14, 8))

    # 创建左侧中文词云图
    plt.subplot(121)
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis('off')

    # 创建右侧原图
    plt.subplot(122)
    plt.imshow(sanguo_mask, interpolation='bilinear')
    plt.axis('off')

    plt.show()


# 读取文件内容
text_path = Path('三国演义.txt')
with text_path.open(encoding='GB18030') as f:
    text_content = f.read()

# 把文件内容交给自定义的split_four_text中文分词函数处理。
sanguo = split_four_text(text=text_content)

# 由于split_four_text函数返回的是一个list类型，词云只接收字符串或者二进制形式输入，
# 所以用str()函数转换为字符串。
draw_wordcloud(text=str(sanguo), image_mask='guanyu_template.jpeg')
