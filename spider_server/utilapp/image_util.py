#coding=utf-8
import os
from PIL import Image
import re
class ImageUitls(object):

    @classmethod
    def image_size_off(cls,rootDir):
        for lists in os.listdir(rootDir):
            # 需要什么格式的图片自己手动改改就好了
            if lists[lists.rfind('.'):].lower() == '.jpg':
                path = os.path.join(rootDir, lists)
                im = Image.open(path)
                # box = cls.clipimage(im.size)
                # region = im.crop(box)
                # size = (130, 150)
                # region.thumbnail(size, Image.ANTIALIAS)
                # 这里保存thumbnail以后的结果
                img = im.resize((100, 123), Image.ANTIALIAS)
                img.save(
                    os.path.join("../app/static/img/low/", lists))
                # region.save(
                #     os.path.join("../app/static/img/low/", lists))
                box = ()

    # 取宽和高的值小的那一个来生成裁剪图片用的box
    # 并且尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间的,个别艺术家有特殊的艺术需求我顾不上
    @classmethod
    def clipimage(cls,size):
        width = int(size[0])
        height = int(size[1])
        box = ()
        if (width > height):
            dx = width - height
            box = (dx / 2, 0, height + dx / 2, height)
        else:
            dx = height - width
            box = (0, dx / 2, width, width + dx / 2)
        return box

def main():
    '''这里输入的参数是图片文件的位置'''
    ImageUitls.image_size_off("../app/static/img/")


if __name__ == '__main__':
    main()