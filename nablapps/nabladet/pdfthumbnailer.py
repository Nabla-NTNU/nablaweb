"""
Contains code for creating a thumbnail of a pdf
"""


def thumbnail_pdf(filename):
    """
    Make a thumbnail of the pdf with the given filename.
    Return the absolute filename of the thumbnail.

    This function needs ImageMagick on the machine.
    """
    from wand.image import Image

    pdf = Image(filename=filename)
    pdf.format = "jpeg"
    thumb_name = filename + ".jpg"
    image = open(thumb_name, "wb")
    pdf.save(file=image)
    return thumb_name
