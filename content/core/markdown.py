from markdown.treeprocessors import Treeprocessor
import markdown
from ..models import ContentImage
import re

from django.template.loader import render_to_string

IMAGE_RE = re.compile(
    r'.*(\[image\:(?P<id>\d+)((\s+align\:(?P<align>right|left))|(\s+size\:(?P<size>small|large|full)))*\s*\]).*',
    re.IGNORECASE)


class ImageClassTree(Treeprocessor):

    def run(self, root):
        if self.markdown.preview:
            for a in root.findall('.//img'):
                a.set('class', 'img-responsive')
        return root


class ImagePreprocessor(markdown.preprocessors.Preprocessor):
    """
    Based on the django wiki implementation
    """

    def run(self, lines):
        new_text = []
        previous_line = ""
        line_index = None
        previous_line_was_image = False
        image = None
        image_id = None
        alignment = None
        caption_lines = []
        for line in lines:
            m = IMAGE_RE.match(line)
            if m:
                previous_line_was_image = True
                image_id = m.group('id').strip()
                alignment = m.group('align')
                size = m.group('size')
                try:
                    image = ContentImage.objects.get(
                        id=image_id)
                except ContentImage.DoesNotExist:
                    pass
                line_index = line.find(m.group(1))
                line = line.replace(m.group(1), "")
                previous_line = line
                caption_lines = []
            elif previous_line_was_image:
                if line.startswith("    "):
                    caption_lines.append(line[4:])
                    line = None
                else:
                    caption_placeholder = "{{{IMAGECAPTION}}}"
                    html = render_to_string(
                        "content/images/render.html",
                        {
                            'image': image,
                            'caption': caption_placeholder,
                            'align': alignment,
                            'size': size
                        })
                    html_before, html_after = html.split(caption_placeholder)
                    placeholder_before = self.markdown.htmlStash.store(
                        html_before,
                        safe=True)
                    placeholder_after = self.markdown.htmlStash.store(
                        html_after,
                        safe=True)
                    new_line = placeholder_before + "\n".join(
                        caption_lines) + placeholder_after + "\n"
                    previous_line_was_image = False
                    if previous_line is not "":
                        if previous_line[line_index:] is not "":
                            new_line = new_line[0:-1]
                        new_text[-1] = (previous_line[0:line_index] +
                                        new_line +
                                        previous_line[line_index:] +
                                        "\n" +
                                        line)
                        line = None
                    else:
                        line = new_line + line
            if line is not None:
                new_text.append(line)
        return new_text


class ImageExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('previewlinks', ImageClassTree(md), "_end")
        md.preprocessors.add('dw-images', ImagePreprocessor(md), '>html_block')


class ContentMarkdown(markdown.Markdown):

    extensions = [ImageExtension()]

    def __init__(self, preview=False, *args, **kwargs):
        kwargs['extensions'] = self.extensions
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.preview = preview


def content_markdown(text, *args, **kwargs):
    md = ContentMarkdown(*args, **kwargs)
    return md.convert(text)
