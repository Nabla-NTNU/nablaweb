# Deployment

I denne mappen ligger filer som kan være til nytte 
under oppsett av nablaweb for produksjon.


Her er noe infor over hva du trenger for å sette opp nabla.no.
Se mer i wikien på bitbucket.org.

## Ting du trenger for å sette opp nablaweb

* Linux server (f.eks ubuntu)
* nginx             (proxy-webserver)
* memcached         (cache-server)
* mysql-server      (database-server)
* libmysqlclient-dev (kompilere python-mysql bindinger via pip)
* python-dev    (kompilere Pillow og python-mysql via pip)
* supervisor
* git
* python 2
* pip
* virtualenv
* bjoern eller gunicorn (wsgi-server)

## Nginx

Bruk nginx-template.conf some en mal til å sette opp nginx.

## Supervisor

Vi bruker supervisor til å starte og stoppe wsgi-server,
for eksempel bjoern eller gunicorn.
Se på supervisor-gunicorn-template.conf for oppsett av dette.

