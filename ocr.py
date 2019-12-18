# from PIL import Image
# # from tesseract import image_to_string
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"/usr/share/tesseract-ocr/tessdata"
# "/usr/share/tesseract-ocr/tessdata"
image_file1="page-1-1.jpg"
filename='/var/www/vhosts/vkingsolutions.com/public_html/clearsight.live/forgery_detection/'+image_file1
# pytesseract.pytesseract.tesseract_cmd = r"/usr/share/tesseract-ocr/tessdata"

# text = pytesseract.image_to_string(Image.open(filename))
# print(text)



import os
myCmd = 'tesseract %s stdout -l eng 3' %(filename)
os.system(myCmd)
myCmd1 = os.popen(myCmd).read()
print(myCmd1)