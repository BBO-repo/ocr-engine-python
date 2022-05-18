from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import numpy as np
import cv2
import io
from ocrize import ocrlib

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/ocr/insurance-card', methods=['POST'])
@limiter.limit("5 per minute")
def insurance_card():

    if "document" not in request.files:
        response = json.dumps({"file": "", "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.CARD, "data": "", "description": "image field not found in body request"}, default=str)
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
        response = json.dumps({"file": document.filename, "status": ocrlib.Types.ProcessingStatus.FAIL, "type": ocrlib.DocType.CARD, "data": "", "description": "could not parse \'image\' field as an image"}, default=str)
        return Response(response=response, status=400, mimetype="application/json")
    else:
        status, ocr_result = ocrlib.OcrImplementations.insurance_card_image_ocr(img)
        response = json.dumps({"file": document.filename, "status": status, "type": ocrlib.DocType.CARD, "data": ocr_result, "description": "ocr process correctly"}, default=str)
        return Response(response=response, status=200, mimetype="application/json")