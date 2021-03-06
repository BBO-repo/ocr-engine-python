import os 
import re
import time

import cv2
import numpy as np
import easyocr
import fitz
import gc
from skimage import restoration, color
from skimage.util import img_as_float, img_as_ubyte

from . import Types

def insurance_card_file_ocr(document_path:str, store_result: bool = False) -> list[Types.ProcessingStatus, str, float]:
    start_time = time.time()
    # return data
    processing_status = Types.ProcessingStatus.WRONG_FILE
    ocr_result = None
    
    # read the image
    img = cv2.imread(document_path)
    # ocr image if not None else return
    if img is not None:
        processing_status, ocr_result = insurance_card_image_ocr(img, store_result)
    
    duration = float(time.time() - start_time)
    # print("{os.path.basename(document_path)}: shape:{str(img.shape)} duration:{duration}")
    # with open("sample.csv", "a") as file_object:
    #    file_object.write(f"{os.path.basename(document_path)}: shape:{str(img.shape)} duration:{duration}")
    #    file_object.write("\n")
    
    del img
    gc.collect()
    return processing_status, ocr_result, duration

def unilab_pdf_file_ocr(document_path:str, store_result: bool = False) -> list[Types.ProcessingStatus, str]:
    start_time = time.time()
    img = get_first_pdf_page_as_image(document_path) 
    processing_status, ocr_result = unilab_pdf_image_ocr(img, store_result, document_path) if img is not None else [Types.ProcessingStatus.WRONG_FILE, None]
    del img
    gc.collect()
    duration = float(time.time() - start_time)
    return processing_status, ocr_result, duration 

def dianalab_pdf_file_ocr(document_path:str, store_result: bool = False) -> list[Types.ProcessingStatus, str]:
    start_time = time.time()
    img = get_first_pdf_page_as_image(document_path)    
    processing_status, ocr_result = dianalab_pdf_image_ocr(img, store_result, document_path) if img is not None else [Types.ProcessingStatus.WRONG_FILE, None]
    del img
    gc.collect()
    duration = float(time.time() - start_time)
    return processing_status, ocr_result, duration

def insurance_card_image_ocr(opencv_image, store_result: bool = False, document_path:str = None) -> list[Types.ProcessingStatus, str]:
    # scale image if width below 1000 pixel
    width = opencv_image.shape[1]
    # scale image if width below 900 pixel
    if width < 900:
        scale = 900/width
        width = int(opencv_image.shape[1] * scale)
        height = int(opencv_image.shape[0] * scale)
        opencv_image = cv2.resize(opencv_image, (width, height), interpolation = cv2.INTER_CUBIC)
    
    # detect blurring
    blurring = cv2.Laplacian(opencv_image, cv2.CV_64F).var()
    blurring_threshold = 300
    # deblurr if below threshold
    if blurring < blurring_threshold:
        # https://stackoverflow.com/questions/20266825/deconvolution-with-opencv
        # https://github.com/opencv/opencv/blob/master/samples/python/deconvolution.py
        # https://github.com/tianyishan/Blind_Deconvolution
        sk_image = img_as_float(opencv_image)
        sk_image_gray = color.rgb2gray(sk_image)
        psf = np.ones((5, 5)) / 25
        
        # restore image using Richardson-Lucy algorithm
        sk_image = restoration.richardson_lucy(sk_image_gray, psf, num_iter=30)
        opencv_image = img_as_ubyte(sk_image)
        #cv2.imwrite("unblurred.png", opencv_image) 
    
    # determine orientation
    #osd = pytesseract.image_to_osd(opencv_image, output_type=pytesseract.Output.DICT)
    #if osd["rotate"] != 0 and osd["orientation_conf"] > 4:
    #    opencv_image = imutils.rotate_bound(opencv_image, angle=osd["rotate"])

    # ocr image
    reader = easyocr.Reader(['fr'],model_storage_directory="/home/EasyOCR/model/", download_enabled=False)
    ocr_result = reader.readtext(opencv_image, detail = 1)
    
    #if store_result and (document_path is not None):
    #    for i, val in enumerate(ocr_result):
    #        start_point = [int(x) for x in val[0][0]] # some time coordinates are return as float so make sur it is an int
    #        end_point = [int(x) for x in val[0][2]]
    #        opencv_image = cv2.rectangle(opencv_image, start_point, end_point, (255, 0, 0), 2)
    #    
    #    name, ext = os.path.splitext(document_path)
    #    file_name = name + '_ocr' + ext
    #    cv2.imwrite(file_name, opencv_image)
    
    # keep only if matching the insurance card number pattern
    card_number_pattern = re.compile('^807')
    match = [ s for s in ocr_result if card_number_pattern.match(s[1])]
    
    response = [Types.ProcessingStatus.SUCCESS, match[0][1].replace(" ", "")] if len(match) else [Types.ProcessingStatus.FAILED, None]
    
    # free easyocr reader
    del match
    del card_number_pattern
    del ocr_result
    del reader
    gc.collect()
    # some card have space in there insurance card number some make sure we remove them
    return response

def unilab_pdf_image_ocr(opencv_image, store_result: bool = False, document_path: str = None) -> list[Types.ProcessingStatus, str]:
    
    # ocr image
    reader = easyocr.Reader(['fr'],model_storage_directory="/home/EasyOCR/model/", download_enabled=False)
    ocr_result = reader.readtext(opencv_image, detail = 1, paragraph=True)
    
    #if store_result and (document_path is not None):
    #   for i, val in enumerate(ocr_result):
    #       start_point = [int(x) for x in val[0][0]] # some time coordinates are return as float so make sur it is an int
    #       end_point = [int(x) for x in val[0][2]]
    #       opencv_image = cv2.rectangle(opencv_image, start_point, end_point, (255, 0, 0), 2)
    #   
    #   name, _ = os.path.splitext(document_path)
    #   file_name = name + '_ocr.png'
    #   cv2.imwrite(file_name, opencv_image)
    
    # retrieve the paragraph containing name and birth date with a regex
    date_pattern = r'\s\d{2}.\d{2}.\d{4}\s\(\D\)\s' # match date dd.mm.yyyy (H)
    match = None
    match_start_index = None
    patient_name = None
    for x in ocr_result:
        match = re.search(date_pattern,x[1])
        if match:
            match_start_index = match.span()[0]
            extracted_text = x[1] 
            patient_name = extracted_text[0:match_start_index]
            break
            
    response = [Types.ProcessingStatus.SUCCESS, patient_name] if match else [Types.ProcessingStatus.FAILED, None]
    del match
    del ocr_result
    del reader
    gc.collect()
    return response

def dianalab_pdf_image_ocr(opencv_image, store_result: bool = False, document_path: str = None) -> list[Types.ProcessingStatus, str]:
    
    # ocr image
    reader = easyocr.Reader(['fr'],model_storage_directory="/home/EasyOCR/model/", download_enabled=False)
    ocr_result = reader.readtext(opencv_image, detail = 1, paragraph=True)
    
    #if store_result and (document_path is not None):
    #  for i, val in enumerate(ocr_result):
    #      start_point = [int(x) for x in val[0][0]] # some time coordinates are return as float so make sur it is an int
    #      end_point = [int(x) for x in val[0][2]]
    #      opencv_image = cv2.rectangle(opencv_image, start_point, end_point, (255, 0, 0), 2)
    #  
    #  name, _ = os.path.splitext(document_path)
    #  file_name = name + '_ocr.png'
    #  cv2.imwrite(file_name, opencv_image)
    
    # retrieve the paragraph containing name and birth date with a regex
    date_pattern = r'\s\d{2}.\d{2}.\d{4}\s\(\D\)\s' # match date dd.mm.yyyy (H)
    match = None
    match_start_index = None
    patient_name = None
    for x in ocr_result:
        match = re.search(date_pattern,x[1])
        if match:
            match_start_index = match.span()[0]
            extracted_text = x[1] 
            patient_name = extracted_text[0:match_start_index]
            break
    
    # dianalabs stores name as Monsieur/Madame Lastname Firstname so remove prefix
    if patient_name:
        patient_name = patient_name.partition(" ")[-1]
    
       
    response = [Types.ProcessingStatus.SUCCESS, patient_name] if match else [Types.ProcessingStatus.FAILED, None]
    del match
    del ocr_result
    del reader
    gc.collect()
    return response

def get_first_pdf_page_as_image(document_path:str):
    
    img = None
    with fitz.Document(document_path) as doc:
        firstPage = doc.load_page(0)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = firstPage.get_pixmap(matrix = mat)
        imgData = pix.tobytes("png")
        nparr = np.frombuffer(imgData, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return img
    