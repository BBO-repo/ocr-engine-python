import os 
import re

import cv2
import easyocr
import pytesseract
import imutils

from . import Types

def insurance_card_file_ocr(document_path:str, store_result: bool = False) -> list[Types.ProcessingStatus, str]:
    # read the image
    img = cv2.imread(document_path)
    # ocr image if not None else return
    return insurance_card_image_ocr(img, store_result) if img is not None else [Types.ProcessingStatus.WRONG_IMAGE, None]

def pdf_unilabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL

def pdf_dianalabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL

def insurance_card_image_ocr(opencv_image, store_result: bool = False, document_path:str = None) -> list[Types.ProcessingStatus, str]:
    # scale image if width below 1000 pixel
    width = opencv_image.shape[1]
    if width < 1000:
        scale = 1000/width
        width = int(opencv_image.shape[1] * scale)
        height = int(opencv_image.shape[0] * scale)
        opencv_image = cv2.resize(opencv_image, (width, height), interpolation = cv2.INTER_CUBIC)
    
    # determine orientation
    osd = pytesseract.image_to_osd(opencv_image, output_type=pytesseract.Output.DICT)
    if osd["rotate"] != 0 and osd["orientation_conf"] > 4:
        opencv_image = imutils.rotate_bound(opencv_image, angle=osd["rotate"])

    # ocr image allowing only numbers
    reader = easyocr.Reader(['fr'],model_storage_directory="/home/EasyOCR/model/", download_enabled=False)
    ocr_result = reader.readtext(opencv_image, detail = 1)
    
    if store_result and (document_path is not None):
        for i, val in enumerate(ocr_result):
            start_point = [int(x) for x in val[0][0]] # some time coordinates are return as float so make sur it is an int
            end_point = [int(x) for x in val[0][2]]
            opencv_image = cv2.rectangle(opencv_image, start_point, end_point, (255, 0, 0), 2)
        
        name, ext = os.path.splitext(document_path)
        file_name = name + '_ocr' + ext
        cv2.imwrite(file_name, opencv_image)
    
    # keep only if matching the insurance card number pattern
    card_number_pattern = re.compile('^807')
    match = [ s for s in ocr_result if card_number_pattern.match(s[1])]
    
    # some card have space in there insurance card number some make sure we remove them
    return [Types.ProcessingStatus.SUCCESS, match[0][1].replace(" ", "")] if len(match) else [Types.ProcessingStatus.FAIL, None]