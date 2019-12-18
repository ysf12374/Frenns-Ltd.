def analysis(filename,resaved,ela):
	from PIL import Image, ImageChops
	from PIL import Image, ImageChops, ImageEnhance
	import sys, os.path
	import os
	#tampered
	# filename = "/home/yousuf/Downloads/original_images/0001 (3).jpg"
	# resaved = filename[:-4] + 'resaved.jpg'
	# resaved="/home/yousuf/Downloads/original_images/"+"0001 (3)"+"resaved.jpg"
	# ela = filename[:-4] + 'ela.png'
	# ela="/home/yousuf/Downloads/original_images/"+"0001 (3)"+"ela.png"
	im = Image.open(filename)
	if im.mode!="RGB":
		im=im.convert("RGB")
	im.save(resaved, 'JPEG', quality=75)#
	resaved_im = Image.open(resaved)
	 
	os.remove(resaved)
	ela_im = ImageChops.difference(im, resaved_im)
	extrema = ela_im.getextrema()
	max_diff = max([ex[1] for ex in extrema])
	scale = 255.0/max_diff

	ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
	ela_im.save(ela)
	im = Image.open(filename)

	im.save(resaved, 'JPEG', quality=95)#
	resaved_im = Image.open(resaved)

	os.remove(resaved)
	ela_im = ImageChops.difference(im, resaved_im)
	extrema = ela_im.getextrema()
	max_diff = max([ex[1] for ex in extrema])
	scale = 255.0/max_diff
	# print(max_diff)
	# print(scale)
	neg=scale-max_diff
	#max diff > 15 original scale <20 original neg  <0
	# max diff <15 tampered scale >20 tampered neg >0
	if neg<0:
	    score1=15
	else:
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
	# print(max_diff,scale,neg)
	return ela_score,max_diff,scale,neg

# if negative<0 and scale<20
# print ("Maximum difference was %d") % (max_diff)

# ela_im.show()
