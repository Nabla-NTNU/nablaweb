# Nablaweb #

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.com).

For å komme i gang med Nablaweb, sjekk [wikien.](https://github.com/NablaWebkom/nablaweb/wiki)

## Systemavhengigheter (ufullstendig)

* python 3.6 (eller nyere)
* pipenv
* npm (nodejs)
* libmagickwand-dev (ImageMagick) (trenges kun dersom du lager et nablad-objekt)

## Mappestruktur ##
- nablapps -- Inneholder alle djangoappene
    - accounts -- Brukere (grunnleggende ting som registrering og profil)
    - album -- For bilder til visning i album
    - blog -- Bloggsystemet
    - bedpres -- Bedriftspresentasjoner, arver fra event
    - com -- Komitesider
    - contact -- For tilbakemelding til Webkom
    - core -- For sentrale funksjoner som ikke hører hjemme i egen app (se egen README)
    - events -- Arrangementer
    - exchange -- For info om utveksling
    - image -- For bilder til bruk i Markdown
    - interactive -- Julekalender, quizer, brukertester og kodegolf
    - jobs -- Stillingsannonser
    - meeting-records -- Styret sine møtereferater
    - nabladet -- pdf-filer av Nabladet
    - nablashop -- Oversikt over ting nabla selger (kompendium, pins, etc.)
    - news -- Nyheter/forsideinnhold, hva som skal vises på forsiden
    - officeBeer -- For bongsystem til kontoret
    - officeCalendar -- For booking av kontoret
    - podcast -- Scråttcast sine podcaster
    - poll -- Avstemninger, bl.a. på forsiden
- templates -- inneholder templates vi har laget, og templates som overskriver
             Django sine.
- nablaweb -- inneholder settings og urls. Knutepunktet for prosjektet.
- var -- variabelt innhold. Inneholder bl.a. media og sqlite.db
- static -- inneholder js, css og noen bilder. 

## Standard mappestruktur i Django (de fleste Django-apps, f.eks. nablapps/accounts) ##
- migrations/ -- lages når man kjører python manage.py makemigrations, ikke gjør manuelle endringer her (med mindre du vet hva du gjør)
- templates/ -- html som definerer struktur og utseende (baseres vanligvis på base.html), bruker variabler gitt fra viewet for dynamiske data
- admin.py -- hvordan klasser i models og forms skal administreres f.eks. i nabla.no/admin
- forms.py -- definerer utfyllingsskjema som kan brukes av view til å ta imot informasjon fra bruker, f.eks. brukerregistering
- models.py -- definerer klasser for appen, f.eks. User som brukes i brukerregistrering (og andre steder...)
- urls.py -- nettaddressen de ulike viewene skal assosieres med
- views.py -- bestemmer hva som skal vises på siden: henter info fra databasen, manipulerer det og kjører en template (context=info til html)

Dette er en veldig overfladisk inføring, fint for rekrutter..
