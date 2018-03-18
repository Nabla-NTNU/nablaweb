from django import template

register = template.Library()

@register.filter
def search_include(value):
    app = value.app_label
    model = value.model_name
    includes_path = "search/includes"
    
    return f"{includes_path}/{app}/{model}.html"


 
