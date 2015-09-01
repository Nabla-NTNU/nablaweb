# Nablaweb #

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.org).

# Hvordan komme i gang med nablaweb #

For å komme i gang med å gjøre nablaweb enda bedre må du få satt opp utviklingsmiljøet ditt.
Her kommer en rask guide for å gjøre det.

Du trenger tilgang til et shell på en Linuxboks. (f.eks en av nablas servere) med følgende installert:

- python 3.4
- pip
- virtualenv


Alle kommandoer du ser fra nå av skal skrives inn i terminalen på den maskinen du jobber på.

## Last ned nablaweb ##
Hvis du ikke allerede har lastet ned koden, kan det gjøres med følgende git-kommando,

```
#!bash

git clone https://bitbucket.org/webkom/nablaweb

```
og tast inn brukernavnet og passordet ditt.
Det skal nå ha dukket opp en mappe som heter nablaweb i den mappen du står i.

## Sett opp virtualenv ##

Nå må du sette opp Python-miljøet ditt og installere alle python-pakkene som trenges til nablaweb.
Til dette bruker vi virtualenv, en python-modul som gjør at du kan ha separate vesjoner av pakker osv. Det er viktig at Python 3.4 brukes, og ikke lavere versjoner, ettersom Python 3.2 og lavere ikke støtter syntaksen u"streng", som brukes av enkelte dependencies. For å sjekke om du har Python 3.4 installert, kjør `python3.4`. Hvis du har Python 3.4 installert, kjør følgende kommando for å lage et virtuelt Python-miljø:

```
#!bash
cd nablaweb/var
virtualenv --python=python3.4 venv

```
Hvis du ikke har Python3.4 installert, men befinner deg på serveren Babel (hvor Nabla.no for øyeblikket kjøres fra), kan du bruke følgende:
```
#!bash
cd nablaweb/var
virtualenv --python=/opt/Python34/bin/python3.4 venv

```
Det skal nå ha blitt laget en ny mappe i mappen du står i som heter `venv`. Der lagres den nye python-executablen din og alle pakkene du laster ned.
Gå gjerne inn på http://virtualenv.readthedocs.org/en/latest/ for å lære mer om virtualenv.

## Aktivere virtualenv ##
For å aktivere det nye miljøet ditt skriver du i Linux
```
#!bash
source venv/bin/activate

```
og i windows
```
#!bash
source venv/Script/activate

```

Nå skal det stå **(venv)** i prompten din.

## Installere nødvendige python-pakker ##
Nå må du installere alle de python-pakkene som trenges for å kjøre nablaweb, for eksemple django.
Gå inn i mappen **nablaweb** ( hvis du ikke allerede har gjort det), og skriv

```
#!bash
pip install -r requirements/devel.txt

```
Skriv inn brukernavn/passord til Bitbucket om nødvendig, ettersom noen av pakkene er private. Pip vil nå laste ned og installere alle pakkene som er nevnt i filen requirements/devel.txt inn i venv-mappen din og en masse tekst vil flagre nedover skjermen.

## Installere bower-pakker ##
Nablaweb bruker også noen front-end-pakker som fås gjennom bower.
```
#!bash
python manage.py bower_install

```

## Sett opp database ##
Vanligvis kjører nablasiden på en mysql-database, men for utvikling bruker vi sqlite3.
For å lage en database og sette opp alle tabeller og felt må du gå inn i mappen nablaweb inne i mappen nablaweb. Det vil si den mappen som har filen manage.py i seg. Og deretter kjøre 
```
#!bash
python manage.py migrate
```
Hvis alt gikk fint skal det nå ha dukket opp en ny fil kalt var/sqlite.db.

## Kjøre nettsiden ##
For å kjøre nettsiden bruker denne kommandoen:

```
#!bash
python manage.py runserver 0.0.0.0:7777
```
Eventuelt hvis du fikk en feilmelding som sier at porten 7777 er opptatt så velger du et annet tall mellom 1024 og 65535.
Det skal nå være mulig å nå din versjon av nablasiden på http://maskin_navn:7777, hvor du bytter ut maskin_navn med det fulle domenenavnet eller ipadressen til maskinen du jobber på. For eksempel for gauss blir dette http://gauss.nabla.no:7777.

## Ferdig oppsatt miljø ##
Neste gang du skal jobbe med nablaweb trenger du bare å aktivere virtualenv og kjøre nettsiden.

Happy coding!

## Mapper ##
De aller fleste undermappene er en egen app, bortsett fra følgende, som er
spesielle mapper:

templates -- inneholder templates vi har laget, og templates som overskriver
             Django sine.

nablaweb -- inneholder settings og urls. Knutepunktet for prosjektet.

w -- relatert til Wikien (burde strengt tatt ikke være i denne mappen trur jeg)