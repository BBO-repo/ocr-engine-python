FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libssl-dev wget git pkg-config\
    python3-dev python3-pip tesseract-ocr libgtk2.0-dev \ 
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# install the python package
COPY . /ocr-engine-python
WORKDIR /ocr-engine-python
RUN pip install .
ENTRYPOINT ["python", "-m", "ocrize"]
