from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os


def pdf_analyze(path):
    path = os.path.abspath(path)
    if path is None:
        return None
    else:
        fp = open(path, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        try:
            return doc.info[0]
        except IndexError as e:
            return None

print(pdf_analyze("/home/kpc/Documents/dolor.pdf"))