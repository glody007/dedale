import qrcode
from reportlab.lib.utils import ImageReader

def imagesQrCodeFromStrings(strings, size):
    '''take list of string and tuple of two elements
    return a list of qr code image generate from
    that strings.'''
    images = []
    for string in strings:
        img = qrcode.make(string)
        resized_image = img.resize(size)
        resized_image.save('tmp.png')
        loaded_image = ImageReader('tmp.png')
        images.append(loaded_image)
    return images
