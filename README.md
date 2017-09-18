# Nablaweb #

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.org).

For å komme i gang med Nablaweb, sjekk wikien på: https://bitbucket.org/webkom/nablaweb/wiki/Home

## Systemavhengigheter (ufullstendig)

* libmagickwand-dev (ImageMagick)
* python 3.4 (eller nyere)
* bower

## Mappestruktur ##
- nablapps -- Inneholder alle djangoappene
- templates -- inneholder templates vi har laget, og templates som overskriver
             Django sine.
- nablaweb -- inneholder settings og urls. Knutepunktet for prosjektet.
- var -- variabelt innhold. Inneholder bl.a. media og sqlite.db
- static -- inneholder js, css og noen bilder. 