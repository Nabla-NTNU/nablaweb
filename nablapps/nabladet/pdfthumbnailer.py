
def thumbnail_pdf(filename):
    from wand.image import Image

    pdf = Image(filename=filename)
    pdf.format = 'jpeg'
    thumb_name = filename + ".jpg"
    image = open(thumb_name, 'wb')
    pdf.save(file=image)
    return thumb_name
