from PIL import Image, ExifTags
# img = Image.open("/home/yousuf/Downloads/page-1-1.jpg")#/media/yousuf/YOUSUF/20190330_131415.jpg

filename="/home/yousuf/Downloads/original_images/20190330_131415.jpg"

img = Image.open(filename)
#exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
# print(exif)
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image
import numpy as np
#import pandas as pd
#import mysql.connector
#import config
#mysql = mysql.connector.connect(
#  host=config.HOST,
#  user=config.USER,
#  passwd=config.PSWD,
#  database = config.CLEARSIGHT_NAME
#  )

#mycursor=mysql.cursor()
#mycursor.execute("SELECT frenns_id FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frenns_id)+"'")
#update=mycursor.fetchall()
DateTime=0
DateTime1=0
DateTimeDigitized=0
DateTimeOriginal=0


exifData = {}
exifDataRaw = img._getexif()
for tag, value in exifDataRaw.items():
    decodedTag = ExifTags.TAGS.get(tag, tag)
    exifData[decodedTag] = value
for key,value in enumerate(exifData):
    if value=="DateTime":
        data=str(exifData[value])
#        print(value,data)
        DateTime=data
    elif value=="DateTimeDigitized":
        data=str(exifData[value])
#        print(value,data) 
        DateTimeDigitized=data
    elif value=="DateTimeOriginal":
        data=str(exifData[value])
#        print(value,data) 
        DateTimeOriginal=data
    elif value=="ExifImageHeight":
        data=str(exifData[value])
#        print(value,data) 
        ExifImageHeight=data
    elif value=="ExifImageWidth":
        data=str(exifData[value])
#        print(value,data) 
        ExifImageWidth=data
    elif value=="ExifVersion":
        data=str(exifData[value])
#        print(value,data) 
        ExifVersion=data
    elif value=="Flash":
        data=str(exifData[value])
#        print(value,data) 
        Flash=data
    elif value=="FocalLengthIn35mmFilm":
        data=str(exifData[value])
#        print(value,data) 
        FocalLengthIn35mmFilm=data
    elif value=="Make":
        data=str(exifData[value])
#        print(value,data)
        Make=data
    elif value=="Model":
        data=str(exifData[value])
#        print(value,data) 
        Model=data
    elif value=="Orientation":
        data=str(exifData[value])
#        print(value,data) 
        Orientation=data
    elif value=="Software":
        data=str(exifData[value])
#        print(value,data) 
        Software=data
    elif value=="WhiteBalance":
        data=str(exifData[value])
#        print(value,data) 
        WhiteBalance=data
    elif value=="YCbCrPositioning":
        data=str(exifData[value])
#        print(value,data)
        YCbCrPositioning=data
    elif value=="LensModel":
        data=str(exifData[value])
#        print(value,data)
        LensModel=data
    elif value=="LensMake":
        data=str(exifData[value])
#        print(value,data)
        LensMake=data



def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

exif = get_exif(filename)
#print(exif)
def get_geotagging(exif):
    if not exif:
#        raise ValueError("No EXIF metadata found")
        print("No EXIF metadata found")
    else:
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
    #                raise ValueError("No EXIF geotagging found")
                    print("No EXIF geotagging found")
                    break
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]

        return geotagging

# exif = get_exif("/media/yousuf/YOUSUF/20190330_131415.jpg")
# geotags = get_geotagging(exif)
# print(geotags)



def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


exif = get_exif(filename)
geotags = get_geotagging(exif)
#print(geotags)
#print(get_coordinates(geotags))
coordinates=str(get_coordinates(geotags))

def make_thumbnail(filename):
    img = Image.open(filename)

    (width, height) = img.size
    if width > height:
        ratio = 50.0 / width
    else:
        ratio = 50.0 / height

    img.thumbnail((round(width * ratio), round(height * ratio)), Image.LANCZOS)
    img.save('thumbnail.jpg')
# thumb=make_thumbnail("/media/yousuf/YOUSUF/20190330_131415.jpg")

# import exif
# photo_path = "/media/yousuf/YOUSUF/20190330_131415.jpg"
# data = exif.parse(photo_path)
# print(data)

import exifread
# Open image file for reading (binary mode)
f = open(filename, 'rb')

# Return Exif tags
tags = exifread.process_file(f)
#print(tags)
printable={}
for key,value in tags.items():
    if key=="GPS GPSVersionID":
        value=str(value)
        print(key,value)
        GPSVersionID=value
    elif key=="Image DateTime":
        value=str(value)
        print(key,value)  
        DateTime1=value
    elif key=="Image GPSInfo":
        value=str(value)
        print(key,value) 
        GPSInfo=value
    elif key=="Image Orientation":
        value=str(value)
        print(key,value) 
        Orientation1=value
    elif key=="Interoperability InteroperabilityIndex":
        value=str(value)
        print(key,value) 
        InteroperabilityIndex=value
    elif key=="Interoperability InteroperabilityVersion":
        value=str(value)
        print(key,value) 
        InteroperabilityVersion=value
    elif key=="Thumbnail Compression":
        value=str(value)
        print(key,value)
        thumbnail_compression=value
    elif key=="Thumbnail ResolutionUnit":
        value=str(value)
        print(key,value) 
        resolution_unit=value
    elif key=="GPS GPSDate":
        value=str(value)
        print(key,value) 
        GPSDate=value
    elif key=="EXIF SceneType":
        value=str(value)
        print(key,value) 
        SceneType=value
    elif key=="EXIF SceneCaptureType":
        value=str(value)
        print(key,value) 
        SceneCaptureType=value
    elif key=="EXIF Flash":
        value=str(value)
        print(key,value)
        Flash1=value
    elif key=="EXIF ExposureMode":
        value=str(value)
        print(key,value)
        ExposureMode=value
    elif key=="EXIF SensingMethod":
        value=str(value)
        print(key,value)
        SensingMethod=value
    if key=="JPEGThumbnail":
        #convert thumbnail(in bytes) to image
#        import io
#        image = Image.open(io.BytesIO(value))
#        image.save(savepath)
        value=str(value)
        printable[key]=value
    try:
        printable[key]=value.printable
    except:
        continue

import json
#metadata={}
#for key,value in exifData.items():
#    if value.__class__==bytes:
#        break
#    else:
#        metadata[key]=value
          

printable = json.dumps(printable)
if DateTime!=0 and DateTime1!=0:
    if DateTime!=DateTime1:
        edited=1
    else:
        datetime=DateTime
if DateTime!=0:
    datetime=DateTime
elif DateTime==0:
    if DateTime1!=0:
        datetime=DateTime1
    elif DateTime1==0:
        if DateTimeDigitized!=0:
            datetime=DateTimeDigitized
        elif DateTimeDigitized==0:
            datetime=0
if datetime==0:
    edited=2;
elif datetime!=0:
    if DateTimeOriginal==0:
        originaldatetime=0
        edited=2
    elif DateTimeOriginal!=0:
        originaldatetime=DateTimeOriginal
        if datetime==originaldatetime:
            edited=0
        else:
            edited=1
    
if DateTime!=0:
    if DateTime1!=0:
        if DateTimeDigitized!=0:
            if DateTimeOriginal!=0:
                if max(DateTime,DateTime1,DateTimeDigitized)!=DateTimeOriginal:
                    edited=1;






        