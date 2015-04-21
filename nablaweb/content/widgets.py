from django.forms import Textarea
from django.utils.safestring import mark_safe


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