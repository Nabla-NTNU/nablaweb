from django.forms import Textarea
from django.utils.safestring import mark_safe, mark_for_escaping


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
                "bower_components/jquery-ui/themes/base/jquery-ui.css",
                "bower_components/font-awesome/css/font-awesome.css"
            )
        }
        js = (
            #"bower_components/jquery/dist/jquery.min.js",
            "bower_components/jquery/jquery.min.js",
            "bower_components/rangy/rangy-core.min.js",
            "bower_components/jquery-ui/ui/minified/jquery-ui.min.js",
            "bower_components/hallo.js/hallo.js",
        )