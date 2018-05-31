import time
from io import BytesIO
from PIL import Image
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_gap(image1, image2):
    """
    获取缺口偏移量
    :param image1: 不带缺口图片
    :param image2: 带缺口图片
    :return:
    """

    left = 120
    for i in range(left, image1.size[0]):
        for j in range(image1.size[1]):
            print(">>>>> i="+str(i)+", j="+str(j))
            if not is_pixel_equal(image1, image2, i, j) \
                    and not is_pixel_equal(image1, image2, i, j+20) \
                    and not is_pixel_equal(image1, image2, i, j+40) \
                    and not is_pixel_equal(image1, image2, i, j+60):
                left = i
                return left
    return left

def is_pixel_equal(image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    print("pixel1(rgb)="+str(pixel1[0])+","+str(pixel1[1])+","+str(pixel1[2]))
    print("pixel2(rgb)="+str(pixel2[0])+","+str(pixel2[1])+","+str(pixel2[2]))
    print("\n")
    threshold = 60
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return False

def calc_cut_offset(full_img, cut_img):

    # cut_img = Image.open(cut_img)
    # full_img = Image.open(full_img)


    x, y = 1, 1
    find_one = False
    top = 0
    left = 0
    right = 0
    threshold = 60
    while x < cut_img.width:
        y = 1
        while y < cut_img.height:
            # cpx = cut_img.getpixel((x, y))
            # fpx = full_img.getpixel((x, y))
            pixel2 = cut_img.load()[x, y]
            pixel1 = full_img.load()[x, y]
            if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                    pixel1[2] - pixel2[2]) < threshold:
                if not find_one:
                    find_one = True
                    x += 60
                    y -= 10
                    continue
                else:
                    if left == 0:
                        left = x
                        top = y
                    right = x
                    break
            y += 1
        x += 1
    return left, right - left



def image_info(image):
    pixel = image.load()
    width = image.size[0]
    height = image.size[1]
    for i in range(width):
        for j in range(height):
            print(pixel[i,j])
            # (r,g,b) = pixel[i,j]
    print("=================")
    print("\r\n")

def find_x(image):

    width = image.size[0]
    print(">>>>> width="+ str(width))
    height = image.size[1]
    print(">>>>> height="+ str(height))

    for i in (60,range(width)):
        for j in range(height):
            pixels = image.load()
            pix = pixels[i,j]
            r = pix[0]
            g = pix[1]
            b = pix[2]

            # print(pixels[i,j])

            # (r,g,b) = pixel[i,j]

    for i in range(width):
        for j in range(height):
            print(pixel[i,j])
            # (r,g,b) = pixel[i,j]
    print("=================")
    print("\r\n")

from PIL import Image
from PIL import ImageChops

def compare_images(path_one, path_two, diff_save_location):
    """
    比较图片，如果有不同则生成展示不同的图片

    @参数一: path_one: 第一张图片的路径
    @参数二: path_two: 第二张图片的路径
    @参数三: diff_save_location: 不同图的保存路径
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)

    diff = ImageChops.difference(image_one, image_two)

    if diff.getbbox() is None:
        # 图片间没有任何不同则直接退出
        return
    else:
        diff.save(diff_save_location)

# if __name__ == '__main__':
#     compare_images('/path/to/瀑布.jpg',
#                    '/path/to/瀑布改.jpg',
#                    '/path/to/不同.jpg')


image1 = Image.open("/Users/Jackie.Liu/DevTools/my_blockchain/test/fullimage.png")
image2 = Image.open("/Users/Jackie.Liu/DevTools/my_blockchain/test/cutimage.png")
# image_info(image1)
# image_info(image2)
# compare_images("/Users/Jackie.Liu/DevTools/my_blockchain/test/fullimage.png", "/Users/Jackie.Liu/DevTools/my_blockchain/test/cutimage.png", "diff.png")

gap = get_gap(image1, image2)
print(">>>>> gap="+str(gap))

# (x, y)=calc_cut_offset(image1, image2)
# print(">>>>> x="+str(x)+", y="+str(y))