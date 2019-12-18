import magic
# all1=magic.detect_from_filename("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg")
# magic.detect_from_filename("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg").mime_type
# print(all1)
# m=magic.open(magic.MAGIC_MIME)
# m.load()
# print(m)
# m.file("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg")
# print(m)
# m.file("/home/yousuf/Downloads/exif-samples-master/jpg/Konica_Minolta_DiMAGE_Z3.jpg")
# print(m)
image_file = open("/home/yousuf/Downloads/original_images/1563977624104.jpg", 'rb').read()
mime = magic.Magic(mime=True)
print(magic.from_buffer(image_file))
file_type=mime.from_buffer(image_file)
all_details=magic.from_buffer(image_file).split(",")
size=all_details[-2]
#import re
#for i in all_details:
#    if re.search('[0-9x]',i):
#        print(re.search('[0-9x]',i))

imgAsString=str(image_file)
xmp_start = imgAsString.find('<x:xmpmeta')
xmp_end = imgAsString.find('</x:xmpmeta')
if xmp_start != xmp_end:
    xmpString = imgAsString[xmp_start:xmp_end+12]
xmp_str = imgAsString[xmp_start:xmp_end+12]
print(xmp_str)
#xmpAsXML = BeautifulSoup( xmpString )
#print(xmpAsXML.prettify())








