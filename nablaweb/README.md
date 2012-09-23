# Nablaweb #

Dette er mappen for alt som er relatert til django. Altså kun kode/templates og
slikt, men ikke statiske filer som .css og .js.

== Et par viktige filer ==
* urls.py -- ruter URLer til den riktige funksjonen i den riktige appen.

* globalsettings.py -- inneholder settings som burde fungere for alle. Om du
                     lager en app, legg den til her.

* settings.py -- Denne filen blir inkludert av Django, og skal inneholde alt som
                 er i globalsettings, i tillegg til personlige innstillinger.

== Mapper ==
De aller fleste undermappene er en egen app, bortsett fra følgende, som er
spesielle mapper:

templates -- inneholder templates vi har laget, og templates som overskriver
             Django sine.

w -- relatert til Wikien (burde strengt tatt ikke være i denne mappen trur jeg)
