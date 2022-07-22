# Python OCR Engine for medical document analysis
## Design
The engine is developed as a python package with an additional Flask web application layer, everything packed in a docker container.<br>
The `Dockerfile` contains all required steps to build and install the python package inside the container and run the web application.<br>

More details are provided in the [`How to use`](#how-to-use) section.

## Requirements
The only requirement is a working docker installation<br>
Tested on:
* Debian 11 bullseye with Docker version 20.10.14
* MacOS Monterey version 12.3.1 with Docker version 20.10.13

## How to use
From a terminal, clone the repository:
```
git clone https://github.com/BBO-repo/ocr-engine-python.git 
```
Build a docker image named for example `ocr_engine` from the `Dockerfile` inside the `ocr-engine-python` directory
```
docker build -t ocr_engine ocr-engine-python
```

Build a container named for example `ocrizer` from the `ocr_engine` generated image
```
docker create --name ocrizer ocr_engine
```

You can now start, stop or restart the generated `ocrizer` container.<br>
From a terminal, enter the following command to start the container in interactive mode
```
docker start --attach -i ocrizer
```
You should have something similar to this displaying in the terminal
```
Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000 (Press CTRL+C to quit)
```
To stop the container just press `CTRL+C`.<br>
You can also run the container in a detached mode, for this enter
```
docker start ocrizer
```
You can check that the container is effectively running by entering
```
docker container ls
```
You should have an output similar to 
```
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS     NAMES
2786a2c25d2f   ocr_engine   "python -m flask run…"   20 minutes ago   Up 20 seconds             ocrizer
```
To stop the container just enter
```
docker stop ocrizer
```
## Check the web application is correctly running
To make sure the web application is correctly running, a sanity endpoint is present in the web application.<br>
Make sure the docker container is running, and send a GET request at `/healthcheck` with the following command:
```
curl --location --request GET 'http://172.17.0.2:5000/healthcheck'
```
You should have a `200` response status with the following
```json
{
  "instanceName": "OcrEngine",
  "instanceVersion": "1.0",
  "environment": "dev"
}
```

## Perform the OCR of a document
To perform the OCR of a document, make sure the container is running and send a `POST` request with a `multipart/form-data` containing a field `document` in the body containing the document you want to analyze.<br>
The `POST` url depends on the kind of document you want to process.<br>
To process a picture of an insurance card the API url is `/ocr/insurance-card`, the full url without any container network redirection should be `http://172.17.0.2:5000/ocr/insurance-card`.


## Running the example
A testing image is provided inside the repository at `ocr-engine-python/example/carte swica 2.png`, the following command lines illustrate a curl command to perform the OCR of the image from a terminal 
```
curl --location --request POST 'http://172.17.0.2:5000/ocr/insurance-card'
--form 'document=@"ocr-engine-python/tests/example/carte swica 2.png"'
```
N.B: make sure the path of the `document` field is correct, it can be a relative or an absolute file path<br>
You should have a result as below:
```json
{
  "file": "carte swica 2.png",
  "status": "SUCCESS",
  "type": "INSURANCE_CARD",
  "data": "80756013841234567890",
  "processing_time": "5.166735649108887sec",
  "description": "ocr process correctly"
}
```

Similarly, you can perform the OCR of a patient examination pdf from Unilabs laboratories to retrieve the patient name with the following request:
```
curl --location --request POST 'http://172.17.0.2:5000/ocr/pdf/unilabs'
--form 'document=@"/path/to/unilabs/pdf/unilabs_patient_examination.pdf"'
```
You should have a result as below:
```json
{
  "file": "unilabs_patient_examination.pdf",
  "status": "SUCCESS",
  "type": "PDF_UNILABS",
  "data": "Name of the patient",
  "processing_time": "10.00339651107788sec",
  "description": "ocr process correctly"
}
```
And the same with Dianalabs patient examination pdf with the following request:
```
curl --location --request POST 'http://172.17.0.2:5000/ocr/pdf/dianalabs'
--form 'document=@"/path/to/dianalabs/pdf/dianalabs_patient_examination.pdf"'
```
You should have a result as below:
```json
{
  "file": "dianalabs_patient_examination.pdf",
  "status": "SUCCESS",
  "type": "PDF_DIANALABS",
  "data": "Name of the patient",
  "processing_time": "11.414628744125366sec",
  "description": "ocr process correctly"
}
```
N.B: the endpoint url for Unilabs OCR WS is `/ocr/pdf/unilabs` whereas for Dianalabs it is `/ocr/pdf/dianalabs`
<!---
## Technical documentation
### Implementation details of the Python package
The python package is called `ocrize` and expects two parameters:<br>
* the type of document, `-t` or `--type`, possible values are:<br>
`1` for insurance card photo<br>
`2` for unilabs pdf document<br>
`3` for dianalabs pdf document<br>
N.B: for the moment only OCR for insurance card photo is implemented
* the path of the document on which ORC is performed, `-p` or `--path`

For example, the `ocrize` package is called inside the docker container with:<br>
```
python -m ocrize -t 1 -p /path/to/insurance/card/photo.png
```
You may need to perform the OCR of a document in your host machine while the document needs to be available inside the docker container.To solve this, you have to mount a volume with the docker container.<br><br>
Let's suppose your document is in your host machine at `/home/usr/data/image.png`, you can mount the folder `/home/usr/data` as a docker volume at `/data` with the `-v /home/usr/data:/data`. The image is now availabe inside the docker container at `/data/image.png`<br><br>
Since the docker container is used as an executable, from your host machine you can perform the OCR of the `image.png` document with the following command run from the terminal, it will create the container name `ocrizer` then call the `ocrize` python module
```
docker run -i -v /home/usr/data:/data --name ocrizer ocr_engine:latest python -m ocrize --type 1 --path /data/image.png
```
You should see the OCR result printed on the terminal as a json content with something like:
```
{"file": "/data/image.png", "status": "ProcessingStatus.SUCCESS", "type": 1, "data": "80756013841234567890"}
```
-->