# Settings #

Django-settings til nablaweb ligger i flere forskjellige filer.

## Settings filer som ligger i repo ##
* base.py inneholder alt som er felles for alle filene. De andre filene importer inn innholdet i base.py.
* devel.py er for for å drive med utvikling.
* production.py er for produksjon

manage.py bruker automatisk devel.py.

## Egne settings-filer ##
Hvis du trenger å bruke din egen settings-fil kan enten gi et ekstra argument --settings til manage.py eller sette miljøvariabelen DJANGO_SETTINGS_MODULE.

For å bruke settings-filen nablaweb/settings/hiasen.py skriver man
```
python manage.py runserver --settings=nablweb.settings.hiasen
```

eller
```
export DJANGO_MODULE_SETTINGS=nablaweb.settings.hiasen
python manage.py runserver
```
