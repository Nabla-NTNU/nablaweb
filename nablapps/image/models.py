"""
Contains a single model called ContentImage
"""
from content.models import BaseImageModel


class ContentImage(BaseImageModel):
    """
    An image associated with some content
    """

    class Meta:
        verbose_name = "Innholdsbilde"
        verbose_name_plural = "Innholdsbilder"
        db_table = "content_contentimage"
