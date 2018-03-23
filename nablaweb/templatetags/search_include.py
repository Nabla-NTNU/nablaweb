from django import template

register = template.Library()
FALLBACK = "generic/generic.html"

@register.filter
def search_include(value):
    app = value.app_label
    model = value.model_name
    includes_path = "search/includes"

    templatename  = f"{includes_path}/{app}/{model}.html"
    
    try:
        template.loader.get_template(templatename)
    except Exception as e:
        print(e)
        templatename = f"{includes_path}/{FALLBACK}"
        
    return templatename
