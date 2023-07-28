from PIL import Image as img
from pdf2image import convert_from_path as CFP
import pytesseract as PT
import fitz
from Queries import *
from ImageData import *
from TextDataClass import *
from pathlib import Path
# from pikepdf import Pdf, Name, PdfImage


# The following function accepts the name of the pdf file and returns the list containing objects of
# text data which contains page number and text on that page
# In the following function the text is extracted per page and the objects of TextData created
# And that objects are inserted in the textObjectsList


def textObjectList(PDF_file):
    pages = CFP(
        PDF_file, poppler_path=r"C:\Users\vaibhav_talap\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin")
    textObjectsList = []
    image_counter = 1
    for page in pages:
        text = str(((PT.image_to_string(page))))
        text = text.replace('-\n', '')
        textObjectsList.append(TextData(image_counter, text))
        image_counter = image_counter + 1
    return textObjectsList


# The following function accepts the name of the pdf file and returns the list containing objects of
# image data which contains page number and image on that page
# In the following function the images are extracted per page and the objects of ImageData created
# And that objects are inserted in the ImageObjectsList

def imageObjectList(PDF_file_1):
    imageObjectsList = []
# open the file
    pdf_file = fitz.open(PDF_file_1)
    for page_index in range(len(pdf_file)):
        # Get the page itself
        page = pdf_file[page_index]
        # Get image list
        image_list = page.get_images()
        # Iterate over the images on the page
        for image_index, imgg in enumerate(image_list, start=1):
            # Get the XREF of the image
            xref = imgg[0]
        # Extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            imageObjectsList.append(ImageData((page_index+1), image_bytes))
    return imageObjectsList


def main():
    PT.pytesseract.tesseract_cmd = r'C:\Users\vaibhav_talap\AppData\Local\Programs\Tesseract-OCR\tesseract'
    PDF_file_1 = r'D:\file_example_PDF_1MB.pdf'

    # Extracting the file Name for a database creation
    dbName = Path(PDF_file_1).stem

    # Calling this function the Database is created as per the name of the file
    createDatabase(dbName)

    textObjectsList = textObjectList(PDF_file_1)
    imageObjectsList = imageObjectList(PDF_file_1)

    # Here we pass the List and the database name to the following function
    # In that the text_table is created and objects from the list are inserted in the text_table.
    insertTextData(dbName, textObjectsList)

    # Here we pass the List and the database name to the following function
    # In that the image_table is created and objects from the list are inserted in the image_table.
    insertImageData(dbName, imageObjectsList)

    # fetchAndStoreImages(dbName)


if __name__ == "__main__":
    main()
