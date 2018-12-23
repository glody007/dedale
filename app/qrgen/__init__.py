import qrcode
from reportlab.lib.utils import ImageReader
from PIL import ImageDraw, Image

def createImagesOfQrCodesAndTitlesFromDatas(datas, size):
    images = []
    for data in datas:
        img = qrcode.make(data['main'])
        resized_image = img.resize(size)
        background = Image.new('RGB', (size[0] + 10, size[1] + 20), color = (255, 255, 255))
        d = ImageDraw.Draw(background)
        d.text((10, size[1]), data['info'], fill=(0, 0, 200))
        background.paste(resized_image, (0, 0))
        background.save('tmp.png')

        loaded_image = ImageReader('tmp.png')
        images.append(loaded_image)

    return images

def createImagesOfQrCodesFromStrings(strings, size):
    '''take list of string and tuple of two elements
    return a list of qr code image generate from
    that strings.'''
    images = []
    for string in strings:
        img = qrcode.make(string)
        resized_image = img.resize(size)
        background = Image.new('RGB', (size[0] + 10, size[1] + 20), color = (255, 255, 255))
        d = ImageDraw.Draw(background)
        d.text((10, size[1]), string, fill=(0, 0, 200))
        background.paste(resized_image, (0, 0))
        background.save('tmp.png')

        loaded_image = ImageReader('tmp.png')
        images.append(loaded_image)

    return images
