# Nablaweb #

Velkommen til nablaweb!

All python-kode, html, css, javascript og andre statiske filer som har med http://nabla.no skal ligge her.

Backenddelen av Nablas nettside er skrevet i [django](http://djangoproject.org).

# Hvordan komme i gang med nablaweb #

For å komme i gang med å gjøre nablaweb enda bedre må du få satt opp utviklingsmiljøet ditt.
Her kommer en rask guide for å gjøre det.

Du trenger tilgang til et shell på en Linuxboks. (f.eks en av nablas servere) med følgende installert:

- python 2.7
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

Nå må du sette opp python-miljøet ditt og installere alle python-pakkene som trenges til nablaweb.
Begynn med å lage et nytt virtuelt python miljø ved å kjøre kommandoen:

```
#!bash
virtualenv my_env

```
Det skal nå ha blitt laget en ny mappe i mappen du står i som heter my_env.
Gå gjerne inn på http://virtualenv.readthedocs.org/en/latest/ for å lære mer om virtualenv.

## Aktivere virtualenv ##
For å aktivere det nye miljøet ditt skriver du
```
#!bash
source my_env/bin/activate

```
Nå skal det stå **(my_env)** i prompten din.

## Installere nødvendige python-pakker ##
Nå må du installere alle de python-pakkene som trenges for å kjøre nablaweb, for eksemple django.
Gå inn i mappen **nablaweb** ( hvis du ikke allerede har gjort det), og skriv

```
#!bash
pip install -r requirements/devel.txt

```
Pip vil nå laste ned og installere alle pakkene som er nevnt i filen requirements/devel.txt nn i my_env-mappen din og en masse tekst vil flagre nedover skjermen.

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
