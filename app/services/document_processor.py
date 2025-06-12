import fitz  # PyMuPDF
import pytesseract # for OCR

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(path):
    """
    Takes a PDF file path as input. It’s designed to extract text from each page of the PDF using OCR.
    :param path: path of document file
    :return: the pages list, containing dictionaries with page numbers and their corresponding extracted text
    """

    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap()  # Converts the current PDF page into a pixmap (pixel map). This generates an image representation of the page for OCR.

        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples) #Creates a PIL Image object from the pixmap’s pixel data.
        text = pytesseract.image_to_string(img, lang="eng+hin")
        pages.append({"page": i, "text": text})
    return pages

def chunk_text(pages, chunk_size=1000, overlap=200):
    """
    Takes a list of page data, a chunk_size, and an overlap.It splits page text into smaller chunks.

    :param pages: list of pag   es containing dictionaries with page numbers and their corresponding extracted text
    :param chunk_size: default = 1000
    :param overlap: default = 200
    :return:
    """

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap) # The splitter to divide text into chunks while maintaining context
    chunks, metadata = [], [] # chunks to store text chunks and metadata to store corresponding metadata

    for p in pages:
        pieces = splitter.split_text(p["text"]) ## Divides the page’s text (p["text"]) into smaller chunks. The split_text method respects the configured chunk_size and overlap.
        for i, chunk in enumerate(pieces):
            chunks.append(chunk)
            metadata.append({"page": p["page"], "chunk_index": i})
    return chunks, metadata
