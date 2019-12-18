from PIL import Image, ImageChops

####################################
# using two images to detect forgery
##################################3#

#ORIG = './books-edited.jpg'
# ORIG = './lottery.jpg'
# TEMP = 'temp.jpg'
# SCALE = 10
# ORIG = "/home/yousuf/Downloads/page-1-1.jpg"
# TEMP = ORIG[:-5] + 'resaved.jpg'
# im = Image.open(ORIG)
# im.save(TEMP, 'JPEG', quality=95)



# def ELA():
#     original = Image.open(ORIG)
#     original.save(TEMP, quality=90)
#     temporary = Image.open(TEMP)

#     diff = ImageChops.difference(original, temporary)
#     d = diff.load()
#     WIDTH, HEIGHT = diff.size
#     for x in range(WIDTH):
#         for y in range(HEIGHT):
#             d[x, y] = tuple(k * SCALE for k in d[x, y])

#     diff.show()

# if __name__ == '__main__':
#     ELA()
##################################

from PIL import Image, ImageChops, ImageEnhance
import sys, os.path
#tampered
filename = "/home/yousuf/Downloads/original_images/0001 (3).jpg"
# resaved = filename[:-4] + 'resaved.jpg'
resaved="/home/yousuf/Downloads/original_images/"+"0001 (3)"+"resaved.jpg"
# ela = filename[:-4] + 'ela.png'
ela="/home/yousuf/Downloads/original_images/"+"0001 (3)"+"ela.png"
im = Image.open(filename)

im.save(resaved, 'JPEG', quality=75)#
resaved_im = Image.open(resaved)
import os 
os.remove(resaved)
ela_im = ImageChops.difference(im, resaved_im)
extrema = ela_im.getextrema()
max_diff = max([ex[1] for ex in extrema])
scale = 255.0/max_diff

ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
print(max_diff)
print(scale)
negative=scale-max_diff
#max diff > 15 original scale <20 original neg  <0
# max diff <15 tampered scale >20 tampered neg >0
if neg<0:
    score1=15
else neg>0:
    score1=1
if  neg<0 and max_diff>15 and scale<20:
    score2=30
elif neg>0 and max_diff<20 and scale>20:
    score2=0
elif neg>0 and max_diff>15 and scale<20:
    score2=10
else:
    score2=4
ela_score=score1+score2
# if negative<0 and scale<20
# print ("Maximum difference was %d") % (max_diff)
ela_im.save(ela)
# ela_im.show()


