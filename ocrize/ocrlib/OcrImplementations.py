import cv2
import easyocr
import re
from . import Types


def insurance_card_ocr(document_path:str, display: bool = False) -> Types.ProcessingStatus:
    
    img = cv2.imread(document_path)
    cv2.imshow('sample image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
    reader = easyocr.Reader(['fr'])
    result = reader.readtext(document_path, detail = 0, allowlist='0123456789')
    card_number_pattern = re.compile('^807')
    match = [ s for s in result if card_number_pattern.match(s) ]

    print(result)
    return Types.ProcessingStatus.SUCCESS

def pdf_unilabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL

def pdf_dianalabs_ocr(document_path:str) -> Types.ProcessingStatus:
    return Types.ProcessingStatus.FAIL