# -*- coding: utf-8 -*-
from quotes.models import Quote
from utils.utility_functions import get_random_item

def random_quote(request):
    """Henter et tilfeldig sitat fra databasen

    Legger random_quote til i alle templates"""

    try:
        quote = get_random_item(Quote)
    except LookupError:
        quote = {"info": "Vi har ingen sitat på lager" }

    return {'random_quote': quote }
