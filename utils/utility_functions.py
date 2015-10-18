def get_random_item(model, max_id=None):
    """Henter et tilfeldig objekt av type model

    Denne funksjonen fungerer selv om noen id-er mangler, og er raskere
    enn SELECT * ORDER BY RAND() LIMIT 1, spesielt for MySQL.
    """
    from django.db.models import Max
    import math
    import random
    
    try:
        if max_id is None:
            max_id = model.objects.aggregate(Max('id')).values()[0]
        min_id = math.ceil(max_id*random.random())
        return model.objects.filter(id__gte=min_id)[0]
    except TypeError:
        raise LookupError("Ingen objekt av den typen eksisterer")


