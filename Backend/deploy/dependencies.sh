#!/bin/bash

sudo apt-get update

sudo apt-get install -y tesseract-ocr libtesseract-dev

sudo wget https://github.com/tesseract-ocr/tessdata/raw/main/pol.traineddata -P /usr/share/tesseract-ocr/4.00/tessdata/

echo "Installing Python packages..."

pip install -r requirements.txt

tesseract --version
