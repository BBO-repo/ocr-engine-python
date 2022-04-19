import cv2
import easyocr
import re
from . import Types
import os

def insurance_card_ocr(document_path:str, store_result: bool = False) -> list[Types.ProcessingStatus, str]:
    
    # read the image
    img = cv2.imread(document_path)
    if img is None:
        return [Types.ProcessingStatus.WRONG_IMAGE, None]

    # scale image if width below 1000 pixel
    width = img.shape[1]
    if width < 1000:
        scale = 1000/width
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        img = cv2.resize(img, (width, height), interpolation = cv2.INTER_CUBIC)


    # ocr image allowing only numbers
    reader = easyocr.Reader(['fr'])
    ocr_result = reader.readtext(img, detail = 1)
    
    if store_result:
        for i, val in enumerate(ocr_result):
            start_point = [int(x) for x in val[0][0]] # some time coordinates are return as float so make sur it is an int
            end_point = [int(x) for x in val[0][2]]
            img = cv2.rectangle(img, start_point, end_point, (255, 0, 0), 2)
        
        name, ext = os.path.splitext(document_path)
        file_name = name + '_ocr' + ext
        cv2.imwrite(file_name, img)
    
    # keep only if matching the insurance card number pattern
    card_number_pattern = re.compile('^807')
    match = [ s for s in ocr_result if card_number_pattern.match(s[1])]
    
    # some card have space in there insurance card number some make sure we remove them
    return [Types.ProcessingStatus.SUCCESS, match[0][1].replace(" ", "")] if match.count else [Types.ProcessingStatus.FAIL, None]

def pdf_unilabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL

def pdf_dianalabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL