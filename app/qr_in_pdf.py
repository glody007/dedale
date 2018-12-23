from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from qrgen import *
from pdfgen.component import Image, Container
from pdfgen.layout import FlowLayout
from pdfgen.exception import OutofBoundError
from pdfgen.document import DefaultDocumentBuilder
from pdfgen.utils import autoVerticalMargin
from pdfgen.component import Margin
from copy import deepcopy

def createComponentsFromImages(images, c):
    '''take group of images and produce group
       of image that come from pdfgen'''
    #c_image means component image
    c_images = []
    for image in images:
        c_image = Image(c, image)
        c_images.append(c_image)
    return c_images

#create pdf that contains list of qrcodes
#qrcodes generated from list of strings passed as arguments
#take list of strings, size of qrcode and path to save pdf
def addQrInPdfFromDatas(datas, size, path):

    images = createImagesOfQrCodesAndTitlesFromDatas(datas, size)
    c = canvas.Canvas(path, pagesize=A4)
    c_images = createComponentsFromImages(images, c)

    documentBuilder = DefaultDocumentBuilder(A4, c)
    for c_image in c_images:
        documentBuilder.addComponent(c_image)
    documentBuilder.createDocument()
