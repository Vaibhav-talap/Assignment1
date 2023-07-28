# Assignment1
This is the user documentation for the Assignment 1.

## Introduction
The assignment written in python to be used for text extraction and image extration from the given PDF.

## Pre-requisites
*   python 3 or newer installed on the system in order to run this assignment
*   The postrgre server must be installed on your system.

## Configuration
The following commands you have to run in your command prompt in order to set up the python virtual environment with appropriate dependancy.

1. pip install virtualenvwrapper-win
2. mkvirtualenv assignment
3. pip install Pillow
4. pip3 install pytesseract
5. pip3 install pdf2image

Now you have to install the tesseract-ocr in your windows machine. You can Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki
and you have to set the variable PT.pytesseract.tesseract_cmd = r'C:\Users\<username>\AppData\Local\Programs\Tesseract-OCR\tesseract' in the Assignment1.py file.
Next you have to download the poppler release. You can download the release from https://github.com/oschwartz10612/poppler-windows/releases
and you have to set the poppler path like poppler_path=r"C:\Users\<username>\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin" in the Assignment1.py file.

# Executing the code 
To activate an environment run "workon assignment"
And run "python Assignment1.py" in order to run the code. 




