# Nablaweb #

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.org).

For å komme i gang med Nablaweb, sjekk wikien på: https://bitbucket.org/webkom/nablaweb/wiki/Home

## Systemavhengigheter (ufullstendig)

* libmagickwand-dev (ImageMagick)
* python 3.4 (eller nyere)
* bower

## Nyttige make-kommandoer:

```
#!bash

make all # Installerer fra pip og kjører migrasjoner
make content # Oppdaterer content-appen til nyeste versjon
make run # Kjører siden på port 1337
make seed # Putter inn test-data i databasen
```

## Mappestruktur ##
De aller fleste undermappene er en egen app, bortsett fra følgende, som er
spesielle mapper:

- templates -- inneholder templates vi har laget, og templates som overskriver
             Django sine.
- nablaweb -- inneholder settings og urls. Knutepunktet for prosjektet.
- var -- variabelt innhold. Inneholder bl.a. media og sqlite.db
- static -- inneholder js, css og noen bilder. 