# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:55:28 2019

@author: Colouree
"""

# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract

###############################################################################
###############################################################################
# filename='/home/yousuf/Downloads/fraud_detection_document/frenn_driv_back_new (copy).JPEG'#frenns_driv.JPEG'
# gray=1
# language='eng'
def ocr_core(filename,gray=0,language='eng'):
    from PIL import Image
    import pytesseract
    import cv2
    import numpy as np
    """
    This function will handle the core OCR processing of images.
    """
    im = cv2.imread(filename, cv2.IMREAD_COLOR)#Image.open(filename)
    if gray==1:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    config=('-l "'+language+'" --oem 1 --psm 3')
    text = pytesseract.image_to_string(im,config=config)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    data= pytesseract.image_to_data(im,config=config)
    print(text)
    print("#"*20)
    print(data)
    print("#"*20)
    text = text.replace('-\n', '')   
    all_txt=text.split('\n')
    return text
###############################################################################
import pandas as pd 
import numpy as np
import mysql.connector
import requests,json

mysql= mysql.connector.connect(
        host="144.76.137.232",
        user="vkingsol_demo",
        passwd="gUj3z5?9",
        database="clearsight_development"  
        )
mycursor=mysql.cursor()
frn_id="FRN00000895"
passport_image=r"C:\Users\Colouree\Desktop\Colouree\perr\20191001_184719.jpg"
match1=ocr_core(passport_image,gray=0,language='eng')
score=0
mycursor.execute("SELECT frenns_id, firstname, lastname, gender, dob, passport_number, ip_address,latitude,longitude FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frn_id)+"' LIMIT 1")
id_details=mycursor.fetchone()

mycursor.close()
mysql.close()
###############################################################################
#allll=[]
#import image_slicer
#bins=image_slicer.slice(filename, 51)
#for i in range(0,len(bins)):
#    temp=bins[i].image
#    open_cv_image = np.array(temp)
#    m = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
#    config=('-l "'+language+'" --oem 1 --psm 3')
#    text = pytesseract.image_to_string(m,config=config)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
##    data= pytesseract.image_to_data(im,config=config)
#    print(text)
#    print("#"*20)
##    print(data)
##    print("#"*20)
#    text = text.replace('-\n', '')   
#    all_txt=text.split('\n')
#    allll.append(all_txt)
###############################################################################
###############################################################################

#filename='/home/yousuf/Downloads/fraud_detection_document/frenns_driv.JPEG'#frenns_driv.JPEG'
#gray=1
#language='eng'
############################################################################
##----------------HIGHLIGHTING TEXT IN AN IMAGE ---------------#
# import cv2
# import pytesseract
# import matplotlib.pyplot as plt


# # read the image and get the dimensions
# img = cv2.imread(filename)
# h, w, _ = img.shape # assumes color image

# # run tesseract, returning the bounding boxes
# boxes = pytesseract.image_to_boxes(img)
# print(pytesseract.image_to_string(img)) #print identified text

# # draw the bounding boxes on the image
# for j,b in enumerate(boxes.splitlines()):
#         b = b.split()
# #        if b[0]=='~':
#         cv2.rectangle(img, ((int(b[1]), h - int(b[2]))), ((int(b[3]), h - int(b[4]))), (0, 255, 0), 2)
# status = cv2.imwrite('frenns_lic_front_detected_new.jpg', img)
# plt.imshow(img)
#--------------------------------------------------------------------#
#######################################################################
    
#color=cv2.imread(filename, cv2.IMREAD_COLOR)

#import numpy as np 
#import cv2 
#from matplotlib import pyplot as plt 
#  
#  
## read the image 
#img = im
#  
## convert image to gray scale image 
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#  
## detect corners with the goodFeaturesToTrack function. 
#corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10) 
#corners = np.int0(corners) 
#  
## we iterate through each corner,  
## making a circle at each point that we think is a corner. 
#for i in corners: 
#    x, y = i.ravel() 
#    cv2.circle(img, (x, y), 3, 255, -1) 
#  
#plt.imshow(img), plt.show() 
#######################################################
#import numpy as np
#import cv2 as cv
#from matplotlib import pyplot as plt
#img = im
#edges = cv.Canny(img,100,200)
#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#plt.show()
###################################################################
#import cv2
#import numpy as np
#im = cv2.imread(filename, cv2.IMREAD_COLOR)
#color=cv2.imread(filename, cv2.IMREAD_COLOR)
#img = color
#gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,120)
#minLineLength = 20
#maxLineGap = 5
#lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
#hori=[]
#vert=[]
#corr_hori_vert=[]
#corr_vert_hori=[]
#for i in lines:
#    x1,y1,x2,y2=i[0][0],i[0][1],i[0][2],i[0][3]
#    if y1==y2 :#and abs(x2-x1)>=20
##        print("horizontal line")
#        hori.append(y1)
#        corr_hori_vert.append(x1)
#    elif x1==x2:# and abs(y2-y1)>=5:
##        print("vertical line")
#        vert.append(x1)
#        corr_vert_hori.append(y1)
#    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#    break
#minimum_hor=min(hori)
#index_hori=hori.index(minimum_hor)
#corr_minimum_hor_vert=corr_hori_vert[index_hori]
#
#minimum_vert=min(vert)
#index_vert=vert.index(minimum_vert)
#corr_minimum_vert_hor=corr_vert_hori[index_vert]
#
#
#maximum_hor=max(hori)
#max_index_hori=hori.index(maximum_hor)
#max_corr_minimum_hor_vert=corr_hori_vert[max_index_hori]
#
#maximum_vert=max(vert)
#max_index_vert=vert.index(maximum_vert)
#max_corr_minimum_vert_hor=corr_vert_hori[max_index_vert]
#
##im[y1:y2, x1:x2]
#roi=gray[minimum_vert:maximum_vert,minimum_hor:maximum_vert]
##roi = gray[corr_minimum_hor_vert:max_corr_minimum_hor_vert, minimum_hor:maximum_hor]
##    break
##cv2.imshow("edges", edges)
#cv2.imshow("lines", roi)
#cv2.waitKey()
#cv2.destroyAllWindows()

###########################################################
#from PIL import Image
#import pytesseract
#import cv2
#import numpy as np
#"""
#This function will handle the core OCR processing of images.
#"""
#im = cv2.imread(filename, cv2.IMREAD_COLOR)#Image.open(filename)
#if gray==1:
#    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#config=('-l "'+language+'" --oem 1 --psm 3')
#text = pytesseract.image_to_string(im,config=config)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
#data= pytesseract.image_to_data(im,config=config)
#
#text = text.replace('-\n', '')   
#all_txt=text.split('\n')
#text=ocr_core('/home/yousuf/Downloads/fraud_detection_document/frenns_driv_back_new.JPEG',1,'eng')
#print(ocr_core('/home/yousuf/Downloads/fraud_detection_document/frenns_driv.JPEG',1,'eng'))#/home/yousuf/Downloads/fraud_detection_document/