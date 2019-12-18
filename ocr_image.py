# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract

def ocr_core(filename):
    from PIL import Image
    import pytesseract
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

#print(ocr_core('/home/yousuf/Downloads/fraud_detection_document/pdf_images/bill_0.jpg'))