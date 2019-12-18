def pdf(pdf,frn_id,name,address,city,post):
    from pdfrw import PdfReader
    from PIL import Image
    # im = Image.open("/home/yousuf/Downloads/per_PPH/pdf_analysis/bill-2018-03-02_2.pdf")
    # im.crop(TranslatePoints(src, pdf, im))
    # print(pdf)
    import os
    from pdfrw import PdfReader, PdfWriter
    from pdfrw.findobjs import page_per_xobj
    
    import sys
    import PyPDF2
    from PIL import Image
    import base64
    import io
    import binascii
    # if (len(sys.argv) != 2):
    #     print("\nUsage: python {} input_file\n".format(sys.argv[0]))
    #     sys.exit(1)
    
    # pdf = "/home/yousuf/Downloads/peepdf-master/85659518.pdf"#85659518
    Extension=pdf[-3:]
    if Extension == 'pdf':
        input1 = PyPDF2.PdfFileReader(open(pdf, "rb"))
        fields=input1.getXmpMetadata()
        info=input1.getDocumentInfo()
        try:
            modified=info['/ModDate']
        except:
            pass
        try:
            created=info['/CreationDate']
        except:
            pass
        try:
            producer=info['/Producer']
        except:
            pass
        if modified and created:
            if modified==created:
                score0=10
            else:
                score0=2
        else:
            score0=0
        # print(input1.getNumPages())
        from pdfminer.pdfparser import PDFParser
        from pdfminer.pdfdocument import PDFDocument
        fp = open(pdf, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        doc.set_parser(parser)
        if len(doc.info) > 0:
        	info1 = doc.info[0]
        num_of_pages=input1.getNumPages()
        # print(num_of_pages)
        try:
            keywords=info1['Keywords']
        except:
            pass
        try:
            author=info1['Author']
        except:
            pass
        score1=0
        score2=0
        score3=0
        ela_score=0
        image_read=0
        image_unread=0
        ela_score1=0
        txt_score=0
        score_inv=0
        blur=0
        from pdf2image import convert_from_path
        pagess=convert_from_path(pdf,500)
        l=0
        text=[]
        detect_name=[]
        detect_address=[]
        detect_city=[]
        detect_post=[]
        for page in pagess:
            file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/document_images",str(frn_id)+str(l) +".jpg")
            page.save(file,'JPEG') 
            l+=1
            import ela
            resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/document_images",str(frn_id)+str(l) +"_resaved.png")
            ela0=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/document_images",str(frn_id)+str(l) +"_ela.png")
            ela_score1,max_diff1,scale1,neg1=ela.analysis(file,resaved,ela0)
            import ocr_image
            try:
                text_sam=ocr_image.ocr_core(file)
            except:
                text_sam=""
            import re
            name=re.search(str(name),text_sam)
            address=re.search(str(address),text_sam)
            city=re.search(str(city),text_sam)
            post=re.search(str(post),text_sam)
            if name:
                detect_name.append(name)
            if address:
                detect_address.append(address)
            if city:
                detect_city.append(city)
            if post:
                detect_post.append(post)
            text.append(text_sam)
            if text:
            	txt_score+=8
            else:
            	txt_score+=0
            if ela_score1:
            	ela_score1+=ela_score1
            else:
            	ela_score1=0
            import image_blur
            blur_score,blur_result=image_blur.blur(file)
            if blur_result==0:
                blur+=10
            elif blur_result==1:
                print("blurry image")
            else:
                blur+=1
        if len(detect_name)>0 or len(detect_address)>0 and len(detect_amount)>0:
            score_inv+=20
        else:
            score_inv+=0
        for i in range(0,num_of_pages):
            page0 = input1.getPage(i)
            if '/XObject' in page0['/Resources']:
                # print("entered xobject")
                xObject = page0['/Resources']['/XObject'].getObject()
                j=0
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        # print("entered subtype",xObject[obj]['/Subtype'])
                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        width,height = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        # print(size)
                        if width<75 or height<75:
                        	score1+=0
                        elif width>=100 and height>=100:
                        	score1+=20
                        elif width>=100 and height<100:
                        	score1+=3
                        elif width<100 and height>=100:
                        	score1+=3
                        else:
                        	score1+=0
    
                        try:
                            data = xObject[obj].getData()
                        except:
                            data = xObject[obj]._data
    #                    print(data)
                        if '/DeviceRGB' in xObject[obj]['/ColorSpace']:# == '/DeviceRGB':
                            # print(j,"rgb")
                            mode = "RGB"
                        elif '/DeviceGray' in xObject[obj]['/ColorSpace']:
                            # print(j,"gray")
                            mode = "P"
                        else:
                            mode = "P"
    #                    data = io.BytesIO(data)
    #                    import cStringIO as StringIO
    #                    stream = StringIO.StringIO(data)
    #                    img = Image.open(data)
    #                    import io
    #                    img = Image.frombytes('RGBA', size, data,'raw')
    #                    file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
    #                    img.save(file)    
                        
                        # mode="RGB"
                        # print(mode,size)
                        # if type(data)==str:
                        # 	data=data.decode('base64')#bytearray(data)
                        try:
    	                    if '/Filter' in xObject[obj]:
    	                        # print("entered '/Filter",xObject[obj]['/Filter'])
    	                        if xObject[obj]['/Filter'] == '/FlateDecode':
    	                            # print("entered111")
    	                            # data=bytearray(data)
    	                            # try:
    	                            img = Image.frombytes(mode, size, data)
    	                            file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".png")
    	                            img.save(file)
    	                            # except:
    	                            # 	file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".jpg")
    	                            # 	img = open(file, "wb")
    	                            # 	img.write(data)
    	                            # 	img.close()
    	                            # img.save(obj[1:] + ".png")
    	                        elif xObject[obj]['/Filter'] == '/DCTDecode':
    	                            # print("entered222")
    	                            file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".jpg")
    	                            img = open(file, "wb")
    	                            img.write(data)
    	                            img.close()
    	                        elif xObject[obj]['/Filter'] == '/JPXDecode':
    	                            # print("entered333")
    	                            file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".jp2")
    	                            img = open(file, "wb")
    	                            img.write(data)
    	                            img.close()
    	                        elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
    	                            # print("entered444")
    	                            file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".tiff")
    	                            img = open(file, "wb")
    	                            img.write(data)
    	                            img.close()
    	                        else:
    	                        	try:
    		                        	img = Image.frombytes(mode, size, data)
    		                        	file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".png")
    		                        	img.save(file)
    		                        except:
    		                        	file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".jpg")
    			                        img = open(file, "wb")
    			                        img.write(data)
    			                        img.close()
    
    	                        image_read+=1
                        except:
                        	image_unread+=1
                        	continue
    
                        # print(mode,size)
                        # try:
                        # img = Image.frombytes(mode, size, data)
                        # except:
                        # 	from io import StringIO
                        # 	img=Image.open(StringIO(data))
                        # img.save(obj[1:] +str(i) +".png")
                        # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                        # img.save(file)
                        # import ela
                        # resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +"_resaved.png")
                        # ela1=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +"_ela.png")
                        # neg=ela.analysis(file,resaved,ela1)
                        # print(neg)
                        # # img = Image.frombytes(mode, size, data)
                        # # img.save(obj[1:] +str(i) +".png")
                        # # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                        # # img.save(file)
    #                    import image_blur
    #                    # resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +"_resaved.png")
    #                    # ela1=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +"_ela.png")
    #                    blur_score=image_blur.blur(file)
    #                    print(file,"entered")
    #                    print("entered")
                        # # img = Image.frombytes(mode, size, data)
                        #         # img.save(obj[1:] +str(i) +".png")
                        # # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                        # # img.save(file)
                        # import ocr
                        # text=ocr.read(file)
                        # if text:
                        # 	print(text)
                        # else:
                        # 	print("no text")
                        try:
                            try:
                                # img = Image.frombytes(mode, size, data)
                                # img.save(obj[1:] +str(i) +".png")
                                # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                                # img.save(file)
                                import ela
                                resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_resaved.png")
                                ela1=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_ela.png")
                                ela_score,max_diff,scale,neg=ela.analysis(file,resaved,ela1)
                                if ela_score:
                                	ela_score+=ela_score
                                else:
                                	ela_score+=0
                            except:
                                # img = Image.frombytes("P", size, data)
                                # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                                # img.save(file)
                                import ela
                                resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_resaved.png")
                                ela1=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_ela.png")
                                ela_score,max_diff,scale,neg=ela.analysis(file,resaved,ela1)
                                print(max_diff,scale,neg);print("safsdfdsfasd")
                                if ela_score:
                                	ela_score+=ela_score
                                else:
                                	ela_score+=0
                                # print(ela_score)
                        except:
                            pass
                        try:
                            try:
                                # img = Image.frombytes(mode, size, data)
                                # img.save(obj[1:] +str(i) +".png")
                                # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                                # img.save(file)
                                import image_blur
                                resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_resaved.png")
                                ela1=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +"_ela.png")
                                blur_score,blur_result=image_blur.blur(file)
                                # print(blur_score,blur_result)
                                if blur_result==0:
                                	score3+=10
                                elif blur_result==1:
                                	score3+=0
                                elif blur_result==2:
                                	score3+=3
                                else:
                                	score3+=0
                            except:
                                # img = Image.frombytes("P", size, data)
                                # file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",obj[1:] +str(i) +".png")
                                # img.save(file)
                                import image_blur
                                blur_score,blur_result=image_blur.blur(file)
                                # print(blur_score,blur_result)
                                if blur_result==0:
                                	score3+=10
                                elif blur_result==1:
                                	score3+=0
                                elif blur_result==2:
                                	score3+=3
                                else:
                                	score3+=0
                        except:
                            pass
    
                    else:
                            try:
                                try:
                                	size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                                	mode="RGB"
                                	try:
                                		data = xObject[obj].getData()
                                	except:
                                		data = xObject[obj]._data
                                	img = Image.frombytes(mode, size, data)
                                	file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".png")
                                	img.save(file)
                                except:
                                	size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                                	mode="RGB"
                                	try:
                                		data = xObject[obj].getData()
                                	except:
                                		data = xObject[obj]._data
    
                                	img = Image.frombytes("P", size, data)
                                	file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"object"+str(i) +".png")
                                	img.save(file)
                            except:
                            	continue
                        # finally:
                        #     print("")
                    j+=1	
            else:
                # print("No image found.")
                kkk=0
        score=ela_score+score1+score2+score3
        score=int(score/num_of_pages)+score0
    #    print(score)
    #    print(image_read,image_unread,score1,ela_score)
        if score>50 and image_unread<=image_read:
        	print("good");result={"result":"good"};return result
        elif score<50 and image_unread<=image_read:
            print("bad")
            result={"result":"bad"}
            return result
        elif image_read<image_unread:
            if score1>0:
                print("good")
                result={"result":"good"}
                return result
            else:
                print("bad")
                result={"result":"bad"}
                return result
        else:
            print("Inconclusive")
            result={"result":"Inconclusive"}
            return result
    
    elif Extension=='jpg' or Extension=='jpeg':
        ela_score_jpg=0
        blur=0
        file=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"jpeg"+str(l) +".jpg")
        import ela
        resaved=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"jpeg"+str(l) +"_resaved.jpg")
        ela2=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/pdf_images",str(frn_id)+"jpeg"+str(l) +"_ela.png")
        ela_score1,max_diff1,scale1,neg1=ela.analysis(file,resaved,ela2)
        import image_blur
        blur_score,blur_result=image_blur.blur(file)
        if blur_result==0:
            blur+=10
        elif blur_result==1:
            print("blurry image")
        else:
            blur+=1
        if ela_score1:
            ela_score_jpg+=ela_score_jpg
        else:
            ela_score_jpg+=0
        if ela_score>=40:
            print("good")
            result={"result":"good"}
            return result
        elif 19<=ela_score<40:
            print("Some anomalies found")
            result={"result":"Some anomalies found"}
            return result
        else:
            print("bad")
            result={"result":"bad"}
            return result
    else:
        result={"error":"Unsupported File Format"}
        return result
