# Python OCR Engine for medical document analysis
## Design
The engine is developed as a python package and is used from docker container called as an executable.<br>
The `Dockerfile` contains all required steps to build and install the python package inside the container.<br>
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
Build a docker image named for example `ocr_engine` from the `Dockerfile` of the repository
```
docker build -t ocr_engine ocr-engine-python
```
As mentionned previously in [`Design`](#design) section, the `ocrize` python package is called as:
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
## Running the example
A testing image is provided inside the repository at `ocr-engine-python/example/carte swica 2.png`, the following command lines illustrate how to perform the OCR of the image from a terminal 
```
git clone https://github.com/BBO-repo/ocr-engine-python.git
```
```
docker build -t ocr_engine ocr-engine-python
```
```
docker run -it -v "/$(pwd)/ocr-engine-python/tests/example":/what/ever/you/want --name ocrizer ocr_engine:latest python -m ocrize --type 1 --path "/what/ever/you/want/carte swica 2.png"
```
You should obtain the following result on the terminal
```
{"file": "/what/ever/you/want/carte swica 2.png", "status": "ProcessingStatus.SUCCESS", "type": 1, "data": "80756013841234567890"}
```
N.B: the docker option `-v` only support absolute path this explains the `/$(pwd)/` prefix when indicating the host folder to mount in the container

## Technical documentation
### Implementation details