"""
Custom markdown processing
"""

import re

from django.template.loader import render_to_string

import markdown

from .models import ContentImage


class ImagePreprocessor(markdown.preprocessors.Preprocessor):
    """
    Preprocesses markdown to find a custom image with optional caption

    Example:
    ```
    [image:123]
        This is a caption for the image.
        Captions are indented 4 spaces after the image tag.
        The captions can be multiline and can contain _markdown_.
    ```

    The images can be interspersed with text on the same line:
    ```
    Look here: [image:123]. Isn't this a nice image?
    ```
    But it only works for one image per line.

    Based on similar code in django wiki.
    """

    # Regular expression which matches a line with a custom image tag
    image_re = re.compile(
        r"(?P<before>.*)"  # Match everything before the image tag
        r"\[image\:(?P<id>\d+)"  # Match id of image
        r"((\s+align\:(?P<align>right|left))|"  # Optional alignment
        r"(\s+size\:(?P<size>small|large|full)))*\s*\]"  # Optional size
        r"(?P<after>.*)",  # Match everything after the image tag
        re.IGNORECASE,
    )
    caption_re = re.compile(r"    (?P<caption>.*)")
    caption_placeholder = "{{{IMAGECAPTION}}}"

    def run(self, lines):
        return list(self.run_iter(lines))

    def run_iter(self, lines):
        """Does the processing as a generator"""
        image_match = None
        caption_lines = None
        for line in lines:
            if image_match:
                caption_match = self.caption_re.match(line)
                if caption_match:
                    caption_lines.append(caption_match.group("caption"))
                    continue
                else:
                    html = self.render_html(image_match)
                    html_before, html_after = html.split(self.caption_placeholder)
                    store = self.md.htmlStash.store
                    yield "".join(
                        [
                            image_match.group("before"),
                            store(html_before),
                            "\n".join(caption_lines),
                            store(html_after),
                            image_match.group("after"),
                        ]
                    )

            image_match = self.image_re.match(line)
            if image_match:
                caption_lines = []
            else:
                yield line

    def render_html(self, match):
        """
        Return a string containing the html for a image with a placeholder for the caption.

        Takes in a re.Match object corresponding to the image_re regular expression.
        """
        image_id = match.group("id")
        alignment = match.group("align")
        size = match.group("size")
        image = ContentImage.objects.filter(
            id=image_id
        ).first()  # Don't fail if image not found

        html = render_to_string(
            "content/images/render.html",
            {
                "image": image,
                "caption": self.caption_placeholder,
                "align": alignment,
                "size": size,
            },
        )
        return html


class ImageExtension(markdown.Extension):
    """
    Class defining the extension to markdown for adding images from ContentImage-model
    """

    def extendMarkdown(self, md: markdown.Markdown) -> None:
        md.preprocessors.register(ImagePreprocessor(md), "dw-images", 5)


def content_markdown(text):
    """Helper function for using the custom markdown"""
    md = markdown.Markdown(extensions=[ImageExtension()])
    return md.convert(text)
