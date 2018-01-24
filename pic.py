# -*- coding:utf-8 -*-
from PIL import Image
import sys
import os


def main(pic):
    # try:
    #     pic      = os.path.abspath(sys.argv[1])  #获取图片路径参数
    # except:
    #     print('指定图片路径')
    img = Image.open(pic)  # 获取图片对象
    width = img.width+60  # 获取图片宽度
    height = img.height  # 获取图片高度
    imgs = img.resize((width, height))
    gray_img = imgs.convert('L')  # 图片转换为'L'模式  模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度

    scale = width // 100  # 图片缩放100长度
    char_lst = ' .:-=+*#%@&$'  # 要替换的字符
    char_len = len(char_lst)  # 替换字符的长度

    for y in range(0, height):  # 根据缩放长度 遍历高度
        for x in range(0, width):  # 根据缩放长度 遍历宽度
            choice = gray_img.getpixel((x, y)) * char_len // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if choice == char_len:
                choice = char_len - 1
            sys.stdout.write(char_lst[choice])  # 写入控制台
        sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    main('code.png')
