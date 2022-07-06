from time import time
from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import numpy as np
import cv2
import fitz
import io
from ocrize import ocrlib
import gc
import time

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/healthcheck')
def healthcheck():
    return Response(response=json.dumps({"instanceName": "OcrEngine", "instanceVersion": "1.0", "environment": "dev"}, default=str), status=200, mimetype="application/json")

@app.route('/ocr/insurance-card', methods=['POST'])
@limiter.limit("60 per minute")
def insurance_card():

    if "document" not in request.files:
        response = json.dumps(
            {"file": "", "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.INSURANCE_CARD, 
             "data": "", "processing_time": "0sec", "description": "document field not found in body request"}
            , default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve image as an opencv image
    # https://gist.github.com/mjul/32d697b734e7e9171cdb
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)    
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # ocr processing of image
    response_status = 400
    if img is None:
        response = json.dumps(
            {"file": document.filename, "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.INSURANCE_CARD, 
             "data": "", "processing_time": "0sec", "description": "could not parse \'document\' field as an image"}, default=str)
    else:
        start_time = time.time()
        status, ocr_result = ocrlib.OcrImplementations.insurance_card_image_ocr(img)
        duration = time.time() - start_time
        response_status = 200 
        response = json.dumps(
            {"file": document.filename, "status": status, "type": ocrlib.DocType.INSURANCE_CARD, 
             "data": ocr_result, "processing_time": f"{duration}sec", "description": "ocr process correctly"}, default=str)
    
    del duration
    del img
    del data
    del in_memory_file
    del document
    gc.collect() 
    return Response(response=response, status=response_status, mimetype="application/json")

@app.route('/ocr/pdf/unilabs', methods=['POST'])
@limiter.limit("60 per minute")
def unilab_pdf():

    if "document" not in request.files:
        response = json.dumps(
            {"file": "", "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.PDF_UNILABS, 
             "data": "", "processing_time": "0sec", "description": "document field not found in body request"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve pdf from request data
    # https://github.com/pymupdf/PyMuPDF/issues/612
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    doc = fitz.open(stream=in_memory_file, filetype="pdf")
    
    # get first page as an opencv image
    firstPage = doc.load_page(0)
    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    pix = firstPage.get_pixmap(matrix = mat)
    imgData = pix.tobytes("png")
    nparr = np.frombuffer(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # ocr processing of image
    response_status = 400
    if img is None:
        response = json.dumps(
            {"file": document.filename, "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.PDF_UNILABS, 
             "data": "", "processing_time": "0sec", "description": "could not parse \'document\' field as a pdf document"}, default=str)
    else:
        start_time = time.time()
        status, ocr_result = ocrlib.OcrImplementations.unilab_pdf_image_ocr(img)
        duration = time.time() - start_time
        response = json.dumps(
            {"file": document.filename, "status": status, "type": ocrlib.DocType.PDF_UNILABS, 
             "data": ocr_result, "processing_time": f"{duration}sec", "description": "ocr process correctly"}, default=str)
        response_status = 200
    
    del start_time
    del img
    del nparr
    del imgData
    del pix
    del mat 
    del firstPage
    del doc
    del in_memory_file
    del document
    gc.collect() 
    
    return Response(response=response, status=response_status, mimetype="application/json")

@app.route('/ocr/pdf/dianalabs', methods=['POST'])
@limiter.limit("60 per minute")
def dianalab_pdf():

    if "document" not in request.files:
        response = json.dumps(
            {"file": "", "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.PDF_DIANALABS, 
             "data": "", "processing_time": "0sec", "description": "document field not found in body request"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve pdf from request data
    # https://github.com/pymupdf/PyMuPDF/issues/612
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    doc = fitz.open(stream=in_memory_file, filetype="pdf")
    
    # get first page as an opencv image
    firstPage = doc.load_page(0)
    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    pix = firstPage.get_pixmap(matrix = mat)
    imgData = pix.tobytes("png")
    nparr = np.frombuffer(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    
    # ocr processing of image
    response_status = 400
    if img is None:
        response = json.dumps(
            {"file": document.filename, "status": ocrlib.ProcessingStatus.FAILED, "type": ocrlib.DocType.PDF_UNILABS, 
             "data": "", "processing_time": "0sec", "description": "could not parse \'document\' field as a pdf document"}, default=str)
    else:
        start_time = time.time()
        status, ocr_result = ocrlib.OcrImplementations.unilab_pdf_image_ocr(img)
        duration = time.time() - start_time
        response = json.dumps(
            {"file": document.filename, "status": status, "type": ocrlib.DocType.PDF_DIANALABS, 
             "data": ocr_result, "processing_time": f"{duration}sec", "description": "ocr process correctly"}, default=str)
        response_status = 200
    
    del img
    del nparr
    del imgData
    del pix
    del mat 
    del firstPage
    del doc
    del in_memory_file
    del document
    gc.collect() 
    
    return Response(response=response, status=response_status, mimetype="application/json")