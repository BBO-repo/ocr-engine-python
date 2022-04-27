# Python OCR Engine for medical document
## Design
The engine is developed as a python package and is used from docker container called as an executable.<br>
The Dockerfile contains all required steps to build and install the python package inside the container.<br>
The python package is called `ocrize` and expects two parameters:<br>
* the type of document, `-t` or `--type`, possible values are:<br>
`1` for insurance card photo<br>
`2` for unilabs pdf document<br>
`3` for dianalabs pdf document<br>
N.B: for the moment only insurance card photo is implemented
* the path of the document on which ORC is performed, `-p` or `--path`

For example, the `ocrize` package is called inside the docker container with:<br>
```
python -m ocrize -t 1 -p /path/to/insurance/card/photo.png
```
More details are provided in the [`How to use`](#how-to-use) section.

## Requirements
Only requires a working docker installation<br>
Tested on:
* Debian 11 bullseye with Docker version 20.10.14
* To be completed

## How to use
From a terminal, clone the repository:
```
git clone https://github.com/BBO-repo/ocr-engine-python.git 
```
Build the docker container that will be named `ocr_engine` from the `Dockerfile` of the repository
```
docker build -t ocr_engine ocr-engine-python/Dockerfile
```
As mentionned previously in [`Design`](#design) section, the `ocrize` python package is called as:
```
python -m ocrize -t 1 -p /path/to/insurance/card/photo.png
```
You may need to perform the OCR of a document in your host machine while the document needs to be available inside the docker container.<br>
To solve this, you have to mount a volume with the docker container..<br><br>
Let's suppose your document is in your host machine at `/home/usr/data/image.png`, you can mount the folder `/home/usr/data` as a docker volume at `/data` with the `-v /home/usr/data:/data`. The image is now availabe inside the docker container at `/data/image.png`


## Technical documentation
### Implementation details