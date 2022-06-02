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

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/healthcheck')
def healthcheck():
    return Response(response=json.dumps({"version": "1.0", "status": "ok"}, default=str), status=200, mimetype="application/json")

@app.route('/ocr/insurance-card', methods=['POST'])
@limiter.limit("60 per minute")
def insurance_card():

    if "document" not in request.files:
        response = json.dumps({"file": "", "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.CARD, "data": "", "description": "document field not found in body request"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve image as an opencv image
    # https://gist.github.com/mjul/32d697b734e7e9171cdb
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)    
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # ocr processing of image
    if img is None:
        response = json.dumps({"file": document.filename, "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.CARD, "data": "", "description": "could not parse \'document\' field as an image"}, default=str)
        response_status = 400
    else:
        status, ocr_result = ocrlib.OcrImplementations.insurance_card_image_ocr(img)
        response_status = 200 
        response = json.dumps({"file": document.filename, "status": status, "type": ocrlib.DocType.CARD, "data": ocr_result, "description": "ocr process correctly"}, default=str)
    
    del img
    del data
    del in_memory_file
    del document
    gc.collect() 
    return Response(response=response, status=response_status, mimetype="application/json")

@app.route('/ocr/pdf/unilab', methods=['POST'])
@limiter.limit("60 per minute")
def unilab_pdf():

    if "document" not in request.files:
        response = json.dumps({"file": "", "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.PDF_UNILAB, "data": "", "description": "document field not found in body request"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve pdf from request data
    # https://github.com/pymupdf/PyMuPDF/issues/612
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    doc = fitz.open(stream=in_memory_file, filetype="pdf")
    
    # get first page as an opencv image
    firstPage = doc.load_page(0)
    zoom = 1
    mat = fitz.Matrix(zoom, zoom)
    pix = firstPage.get_pixmap(matrix = mat)
    imgData = pix.tobytes("png")
    nparr = np.frombuffer(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    
    # ocr processing of image
    if img is None:
        response = json.dumps({"file": document.filename, "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.PDF_UNILAB, "data": "", "description": "could not parse \'document\' field as a pdf document"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    else:
        status, ocr_result = ocrlib.OcrImplementations.unilab_pdf_image_ocr(img)
        response = json.dumps({"file": document.filename, "status": status, "type": ocrlib.DocType.PDF_UNILAB, "data": ocr_result, "description": "ocr process correctly"}, default=str)
        return Response(response=response, status=200, mimetype="application/json")

@app.route('/ocr/pdf/dianalab', methods=['POST'])
@limiter.limit("60 per minute")
def dianalab_pdf():

    if "document" not in request.files:
        response = json.dumps({"file": "", "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.PDF_DIANALAB, "data": "", "description": "document field not found in body request"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    
    # retrieve pdf from request data
    # https://github.com/pymupdf/PyMuPDF/issues/612
    document = request.files["document"]
    in_memory_file = io.BytesIO()
    document.save(in_memory_file)
    doc = fitz.open(stream=in_memory_file, filetype="pdf")
    
    # get first page as an opencv image
    firstPage = doc.load_page(0)
    zoom = 1
    mat = fitz.Matrix(zoom, zoom)
    pix = firstPage.get_pixmap(matrix = mat)
    imgData = pix.tobytes("png")
    nparr = np.frombuffer(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    
    # ocr processing of image
    if img is None:
        response = json.dumps({"file": document.filename, "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.PDF_DIANALAB, "data": "", "description": "could not parse \'document\' field as a pdf document"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    else:
        status, ocr_result = ocrlib.OcrImplementations.dianalab_pdf_image_ocr(img)
        response = json.dumps({"file": document.filename, "status": status, "type": ocrlib.DocType.PDF_DIANALAB, "data": ocr_result, "description": "ocr process correctly"}, default=str)
        return Response(response=response, status=200, mimetype="application/json")