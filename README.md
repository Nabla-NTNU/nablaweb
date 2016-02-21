# Nablaweb #

## Systemavhangigheter (ufullstendig)

* libmagickwand-dev (ImageMagick)

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.org).

For å komme i gang med Nablaweb, sjekk wikien på: https://bitbucket.org/webkom/nablaweb/wiki/Home

Nyttige make-kommandoer:

'''
#!bash

make all # Installerer fra pip og kjører migrasjoner
make content # Oppdaterer content-appen til nyeste versjon
make run # Kjører siden på port 1337
make seed # Putter inn test-data i databasen
'''
