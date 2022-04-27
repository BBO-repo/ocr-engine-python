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

For example, the `ocrize` package is called with<br>
```
python -m ocrize -t 1 -p /path/to/insurance/card/photo.png
```
More details provided in the [`How to use`](#how-to-use) section.

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
## Technical documentation