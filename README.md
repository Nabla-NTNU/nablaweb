# Nablaweb #

Velkommen. Sjekk wikien for nytting informasjon om bl.a. Git.

# Finner ikke settings.py? #
    cd nablaweb
    vim settings.py
Skriv:

    from globalsettings import *

Dette er slik at alle kan ha sine personlige settings.


# Missing columns? #
Vi bruker South, noe som fører til at du må gjøre dette:

    rm sqlite.db
    cd nablaweb
    ./manage.py syncdb --all

# Fungerer ikke css-en? #
Vi bruker Twitter-Bootstrap, som må kompileres fra LESS til CSS. Skriv i /nablaweb:

    make

