# Static #

Om admin-delen mangler bilder, er kanskje symlinken til admin-static-filene
feil. Da må du gjøre noe lignende dette:

rm -r admin
ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin .


Denne mappen inneholder statiske filer, som er tilgjengelige mot web på 
f.eks. /static/.

Kun små filer skal puttes i denne mappen. Store mediefiler skal ikke puttes i repositoriet!

