# -*- coding: utf-8 -*-
""" Skript som overfører brukere fra gamle Nablanettside til ny
Krever at den ligger i samme mappe som settings.py"""
import MySQLdb
import MySQLdb.cursors
import pprint
from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.contrib.auth.models import User,Group
from accounts.models import UserProfile

def totnavn_til_delt(totnavn):
    index = 0
    index2=totnavn.find(" ", index)
    while(index2 != -1):
        index = index2
        index2=totnavn.find(" ", index+1)
    return totnavn[:index],totnavn[index+1:]

def ordne_opp(g_bruker):
    g_bruker['totnavn'] = unicode(g_bruker['totnavn'].decode('cp1252'))
    g_bruker['adresse'] =  unicode(g_bruker['adresse'].decode('cp1252'))
    g_bruker['profil'] =  unicode(g_bruker['profil'].decode('cp1252'))

def slett():
    User.objects.exclude(username='hiasen').delete()

db = MySQLdb.connect(user="nabla",passwd="Ls29RA9PrdJr92ru",db="nabla_web", cursorclass=MySQLdb.cursors.DictCursor)

c=db.cursor()
c.execute("""SELECT totnavn,brukernavn,mail,kull,profil,adresse,postnr,poststed,bursdag,mobil, telefon ,nullvektor,ikke_kullmail, kortnummer, passord FROM `brukere` WHERE 
    `kull`>=2007 OR
    sist_aktiv >='2010-09-01'""")

aktive_brukere=c.fetchall()
c.execute("""SELECT totnavn,brukernavn,mail, kull,nullvektor,ikke_kullmail FROM `brukere` WHERE 
    `kull`<2007 AND
    sist_aktiv <'2010-09-01'""")

inaktive_brukere=c.fetchall()

komponenter,new = Group.objects.get_or_create(name='komponenter')
if new:
    komponenter.save()

kull = {}
for g_bruker in aktive_brukere:
    ordne_opp(g_bruker)
    u = User.objects.get_or_create(username=g_bruker['brukernavn'])[0]
    u.email = g_bruker['mail']
    u.first_name,u.last_name = totnavn_til_delt(g_bruker['totnavn'])
    #u.password = g_bruker['passord']
    u.set_password("foobar")
    if not(g_bruker['nullvektor']):
        komponenter.user_set.add(u)
    u.save()
    komponenter.save()

    if not(g_bruker['kull'] is None):
      kullet,new = Group.objects.get_or_create(name="kull"+str(g_bruker['kull']))
      kullet.save()
      kullet.user_set.add(u)
      
    profil =UserProfile.objects.get_or_create(user = u)[0]
    if not(g_bruker['bursdag'] is None):
        profil.birthday = g_bruker['bursdag']
    if not(g_bruker['telefon'] is None):
        profil.telephone = g_bruker['telefon']
    if not(g_bruker['mobil'] is None):
        profil.cell_phone = g_bruker['mobil']
    if not(g_bruker['adresse'] is None):
        profil.address = g_bruker['adresse']
    if not(g_bruker['postnr'] is None):
        profil.mail_number = g_bruker['postnr']
    if not(g_bruker['profil'] is None):
        profil.about = g_bruker['profil']
    #if not(g_bruker['kortnummer'] is None):
    #    profil.ntnu_card_number = g_bruker['kortnummer']
    profil.save()
'''
for g_bruker in inaktive_brukere:
    g_bruker['totnavn'] = unicode(g_bruker['totnavn'].decode('cp1252'))
    u = User.objects.get_or_create(username=g_bruker['brukernavn'])[0]
    if g_bruker['mail'] is None:
        print u
        print inaktive_brukere.index(g_bruker)
    else:
        u.email = g_bruker['mail']
    u.first_name,u.last_name = totnavn_til_delt(g_bruker['totnavn'])
    u.is_active = False
    u.save()
    if not(g_bruker['nullvektor']):
        komponenter.user_set.add(u)
        komponenter.save()
'''

c.execute("""SELECT brukere.brukernavn, stillinger.id, stillinger.tittel
    FROM  `stillinger_kart` ,  `brukere` ,  `stillinger` 
    WHERE stillinger_kart.stilling = stillinger.id
    AND brukere.id = stillinger_kart.bruker""")

stillingsresultat = c.fetchall()

stillinger = {}

for x in stillingsresultat:
    stillinger.setdefault(x['id'],[]).append(x['brukernavn'])


for x in kull:
    x.group_type = "kull"


komiteer = {
1:Group.objects.get_or_create(name='Leder')[0],
2:Group.objects.get_or_create(name='Sekretaer')[0],
3:Group.objects.get_or_create(name='Kasserer')[0],
4:Group.objects.get_or_create(name='BN-leder')[0],
5:Group.objects.get_or_create(name='Festsjef')[0],
6:Group.objects.get_or_create(name='Kjellersjef')[0],
7:Group.objects.get_or_create(name='Ambassador')[0],
8:Group.objects.get_or_create(name='Nestleder')[0],
9:Group.objects.get_or_create(name='Redaktor')[0],
10:Group.objects.get_or_create(name='Websjef')[0],
11:Group.objects.get_or_create(name='BN')[0],
12:Group.objects.get_or_create(name='Festkom')[0],
13:Group.objects.get_or_create(name='Kjellerstyret')[0],
14:Group.objects.get_or_create(name='Edukom')[0],
15:Group.objects.get_or_create(name='Redaksjonen')[0],
16:Group.objects.get_or_create(name='Webkom')[0],
}

for x in range(1,17):
    komite = komiteer[x]
    if x <=10:
        komite.group_type = "stilling";
    else:
        komite.group_type = "komite";
    komite.save()
    print(komite)
    brukere = stillinger[x]
    for bruker in brukere:
        print bruker
        django_bruker = User.objects.get(username=bruker)
        django_bruker.is_staff = True
        if komite.name =='Webkom': 
            django_bruker.is_superuser = True
        django_bruker.save()

        komite.user_set.add(django_bruker)
    komite.save()
