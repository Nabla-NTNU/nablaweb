from django.utils.encoding import force_text
from django.forms import Textarea, SelectMultiple
from django.utils.safestring import mark_safe


class MultipleImagesChooser(SelectMultiple):

    def render_option(self, selected_choices, option_value, option_label):
        selected_html = ''
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        return "<option value=\"{value}\" data-img-src=\"{src}\">{label}</option>".format(
            value=option_value, label=force_text(option_label), src=option_label, selected=selected_html)

    def render(self, name, value, attrs={}, choices=()):
        html = super(MultipleImagesChooser, self).render(name, value, attrs, choices)
        html += """
        <style>
        ul.thumbnails.image_picker_selector li .thumbnail img {{
            max-width: 150px;
            max-height: 150px;
        }}
        </style>
        <script type="text/javascript">
        jQuery("select[name='{name}']").imagepicker({{
            show_label: true,
            hide_select: false
        }});
        </script>
        """.format(name=name)
        return mark_safe(html)

    class Media:
        css = {
            "all": (
                "image-picker/image-picker.css",
            )
        }
        js = (
            "jquery/jquery.min.js",
            "image-picker/image-picker.min.js",
        )


class MarkdownEditor(Textarea):

    def render(self, name, value, attrs=None):

        html = Textarea.render(self, name, value, attrs={'hidden': "true", "class": "editable"})

        html += """
        <p class="editable"></p>
        <script type="text/javascript">
        jQuery(function () {
        var textarea = jQuery('[name="""+name+"""]').get(0);
        jQuery('.editable').hallo({
            plugins: {
               'halloformat': {},


            }
        });

        textarea.form.onsubmit = function() {
            textarea.value = jQuery('.editable').text();
        };
        });
        </script>
        """
        return mark_safe(html)

    class Media:
        css = {
            "all": (
                "jquery-ui/themes/base/jquery-ui.css",
                "font-awesome/css/font-awesome.css"
            )
        }
        js = (
            # "jquery/dist/jquery.min.js",
            "jquery/jquery.min.js",
            "rangy/rangy-core.min.js",
            "jquery-ui/ui/minified/jquery-ui.min.js",
            "hallo.js/hallo.js",
        )
