FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libssl-dev wget git pkg-config\
    python3-dev python3-pip tesseract-ocr libgtk2.0-dev unzip\ 
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# install the python package
COPY . /ocr-engine-python
WORKDIR /ocr-engine-python
# install python packages
RUN pip install . && \
# download detection and recognition models
wget https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip && \
wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/latin_g2.zip && \
# build model directory
mkdir -p /home/EasyOCR/model/ && \
# unzip model files to model directory
unzip craft_mlt_25k.zip -d /home/EasyOCR/model/ && \
unzip latin_g2.zip -d /home/EasyOCR/model/

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]