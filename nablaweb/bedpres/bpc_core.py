# -*- coding: utf-8 -*-

import inspect
import re # Validering av tidspunkt som strenger
import json # BPC returnerer json
from urllib import urlencode
from urllib2 import urlopen, Request, URLError
from datetime import datetime


# Samleunntak.
class BPCException(Exception):
    def __init__(self, message):
        super(BPCException, self).__init__(message)

# Unntak som skyldes feil generert her.
class BPCClientException(BPCException):
    def __init__(self, message):
        super(BPCClientException, self).__init__(message)

# Feil som skyldes BPC.
class BPCResponseException(BPCException):
    def __init__(self, message, response):
        super(BPCResponseException, self).__init__(message)
        self.response = response


# Datoformatet brukt av BPC. ISO8601!
BPC_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Gamle URL'er til BPC-serveren.
#BPC_URL = 'https://bpc.timini.no/bpc/remote/'
#BPC_URL = 'https://bpc.timini.no/bpc_testing/remote/' # Testserver

# Nye URL'er til BPC-serveren.
#BPC_URL = 'https://www.bedriftspresentasjon.no/remote/'
BPC_URL = 'http://testing.bedriftspresentasjon.no/remote/' #Testserver

# Informasjon som må sendes med hver forespørsel.
SETTINGS = {
    'forening': '3',
    'key': 'a88fb706bc435dba835b89ddb2ba4debacc3afe4',
#    'key': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'method': 'json',
    'debug': 'false',
    'timing': 'false',
    'version': '1.5',
    }

# Informasjon om typer forespørsler.
# Brukes for å validere forespørsler før de sendes.
REQUESTS = {
    'get_events':
        {'required': (),
         'optional': ('event', 'username', 'fromdate', 'todate', 'event_type')},
    'add_attending':
        {'required': ('fullname', 'username', 'card_no', 'event', 'year'),
         'optional': ('user_id',)},
    'rem_attending':
        {'required': ('event', 'username'),
         'optional': ()},
    'get_attending':
        {'required': ('event',),
         'optional': ('sort',)},
    'get_waiting':
        {'required': ('event',),
         'optional': ('sort',)},
    'get_user_stats':
        {'required': ('username',),
         'optional': ('detailed_stats', 'fromdate', 'todate', 'event_type')},
    'get_event_stats':
        {'required': (),
         'optional': ('fromdate', 'todate', 'event_type', 'attended', 'show_waitlist')},
    }

# Typer feil som BPC kan rapportere om.
BPC_ERRORS = {
    # Fatalt - Disse avbryter skriptet.
    '101': 'Feil eller ingen handshake',
    '102': 'Feil eller ingen request',
    '103': 'Ingen eller ikke-eksisterende event',
    '104': 'Feil i SQL-spørring',
    '105': 'Feil eller ikke noe brukernavn gitt',
    '106': 'Feil eller ikke noe fullstendig navn gitt',
    '107': 'Feil eller ikke noe kortnummer gitt',
    '108': 'Feil versjon av integrasjonskoden',
    '109': 'Handshake støtter ikke denne operasjonen',

    # Feil - Alvorlige feil som ikke bør skje med en korrekt oppsatt
    # klient, men ikke så alvorlige at skriptet avbrytes. En fatal
    # feil vil ofte følge etter en vanlig feil, disse kan da hjelpe
    # til å spore problemet.
    '201': 'Feil i validering av en parameter',
    '202': 'Du har ikke tilgang til å gjøre dette',
    '203': 'PHP-feil i scriptet på serveren',
    '204': 'Manglende JSONP-callbackparameter, kan ikke returnere data',

    # Tilbakemeldinger - Dette er vanlige tilbakemeldinger som kan
    # komme og som bør tas høyde for ved bruk av funksjonene gitt i
    # parantes.
    '401': 'Studenten går ikke på høyt nok årstrinn for dette arrangementet',
    '402': 'Det finnes ikke ledige plasser på dette arrangementet',
    '403': 'Det finnes ingen arrangementer som passer med denne forespørselen',
    '404': 'Det finnes ingen deltagere som passer med denne forespørselen',
    '405': 'Personen (kortnummer eller brukernavn) er allerede påmeldt dette arrangementet',
    '406': 'Brukernavnet er ikke påmeldt dette arrangementet og kan dermed ikke meldes av',
    '407': 'Brukeren var ikke påmeldt som medlem av denne linjeforeningen, og kan dermed ikke meldes av',
    '408': 'Påmelding har ikke startet ennå',
    '409': 'Påmeldingsfristen har passert',
    '410': 'Studenten går i et for høyt årstrinn for dette arrangementet.',
    }


# Valider spørringen før den sendes.
def _validate_parameter(parameter, value):
    if type(parameter) is not str and type(parameter) is not unicode:
        raise BPCClientException("'%s': Parameter names must be type 'str' or 'unicode', not '%s'." % (parameter, type(parameter)))
    elif type(value) is not str and type(value) is not unicode:
        raise BPCClientException("'%s': Value must be type 'str' or 'unicode', not '%s'." % (value, type(value)))
    elif parameter == 'request' and value not in REQUESTS:
        raise BPCClientException("'%s' is not a valid request type." % value)
    elif parameter == 'sort' and value not in ['lname', 'fname', 'username', 'registered']:
        raise BPCClientException("'%s' is not a valid value for 'sort'." % value)
    elif parameter == 'fromdate' or parameter == 'todate':
        try:
            datetime.strptime(value, BPC_TIME_FORMAT)
        except ValueException:
            raise BPCClientException("'%s' is not a valid time in the format '%s'." % (value, BPC_TIME_FORMAT))
    elif parameter == 'card_no':
        p = re.compile('^[A-Fa-f0-9]{40}$') # SHA-1
        if not p.match(value):
            raise BPCClientException("'%s' is not a valid sha1 hash." % value)


# Lag en dict som tilsvarer en gyldig spørring ved å kopiere
# nødvendige felt over i en ny dict, sammen med innstillinger.
# På den måten sendes kun relevant informasjon.
def _create_valid_request(data):
    request = SETTINGS.copy()

    def _copy_parameters(parameters, raise_error, error_msg):
        for parameter in parameters:
            try:
                request[parameter] = data[parameter].encode('utf-8')
                _validate_parameter(parameter, data[parameter])
            except KeyError:
                if raise_error:
                    raise BPCClientException(error_msg % parameter)

    _copy_parameters(['request'], raise_error=True, error_msg="Parameter '%s' is required.")
    _copy_parameters(REQUESTS[request['request']]['required'], raise_error=True, error_msg="Parameter '%s' is required for request type '%s'." % ('%s', request['request']))
    _copy_parameters(REQUESTS[request['request']]['optional'], raise_error=False, error_msg=None)

    return request


# _make_request kalles av en metode med et navn som er en gyldig verdi
# for 'request', for gjøre en forespørsel av denne
# typen. _make_request skal altså ikke brukes direkte. Ansvaret for
# sjekking av at nødvendige argument er med flyttes dermed fra Python
# sin funksjonskallmekanisme til _create_valid_request.
def _make_request(**request):
    request['request'] = inspect.stack()[1][3]

    # TODO: Sjekk hvilke unntak som risikeres fra urlencode og urlopen.
    validated_request = _create_valid_request(request)
    answer = Request(BPC_URL, urlencode(validated_request))

    try:
        fd = urlopen(answer)
        raw_data = fd.read()
    except URLError:
        raise BPCClientException("Could not contact server.")
    finally:
        fd.close()

    response = json.loads(raw_data)

    if 'error' in response:
        error_id = response['error'][0].keys()[0]
        raise BPCResponseException(BPC_ERRORS[error_id], response)

    return response


def get_events(**request): return _make_request(**request)
def add_attending(**request): return _make_request(**request)
def rem_attending(**request): return _make_request(**request)
def get_attending(**request): return _make_request(**request)
def get_waiting(**request): return _make_request(**request)

def bpc_time_to_datetime(bpc_time):
    return datetime.strptime(bpc_time,BPC_TIME_FORMAT)

if __name__ == '__main__':
    print get_events()
#{u'event': [{u'count_waiting': u'0', u'description_formatted': u'<p>Schlumberger Oilfield Services er petroleumsindustriens ledende leverand\xf8r av kompetanse og teknologiske l\xf8sninger innen utforskning og produksjon.</p>\n\n<p>Konsernet har over 100.000 ansatte fra 140 ulike nasjonaliteter i over 80 land.</p>\n\n<p>Schlumberger ble etablert i Norge allerede i 1966 og i dag befinner selskapets teknologiske kompetanse seg ved basene i Stavanger, Bergen og Oslo, med totalt 2.400 personer.</p>\n', u'waitlist_enabled': u'1', u'description': u'Schlumberger Oilfield Services er petroleumsindustriens ledende leverand\xf8r av kompetanse og teknologiske l\xf8sninger innen utforskning og produksjon.\r\n\r\nKonsernet har over 100.000 ansatte fra 140 ulike nasjonaliteter i over 80 land.\r\n\r\nSchlumberger ble etablert i Norge allerede i 1966 og i dag befinner selskapets teknologiske kompetanse seg ved basene i Stavanger, Bergen og Oslo, med totalt 2.400 personer.', u'is_advertised': u'1', u'title': u'Schlumberger', u'registration_start': u'2012-02-21 12:00:00', u'seats_available': 37, u'seats': u'50', u'min_year': u'3', u'open_for': u'3', u'place': u'R5', u'registration_started': u'1', u'web_page': u'http://www.slb.com/', u'time': u'2012-02-28 18:15:00', u'deadline_passed': u'0', u'deadline': u'2012-02-27 12:00:00', u'max_year': u'5', u'id': u'324', u'logo': u'http://bpc.timini.no/logo/bedpres.png', u'this_attending': u'13'}, {u'count_waiting': u'0', u'description_formatted': u'<p>Accenture is a global management consulting, technology services and outsourcing company, with more than 223,000 people serving clients in more than 120 countries. Combining unparalleled experience, comprehensive capabilities across all industries and business functions, and extensive research on the world\u2019s most successful companies, Accenture collaborates with clients to help them become high-performance businesses and governments. The company generated net revenues of US$21.6 billion for the fiscal year ended Aug. 31, 2010.</p>\n\n<p>Accenture inviterer til bedriftspresentasjon for siv.ing Fysikk og Matematikk klokken 17:15 i R8 p\xe5 realfagsbygget.</p>\n\n<p>Bespisning: Asiatisk buffet p\xe5 Kos</p>\n', u'waitlist_enabled': u'0', u'description': u'Accenture is a global management consulting, technology services and outsourcing company, with more than 223,000 people serving clients in more than 120 countries. Combining unparalleled experience, comprehensive capabilities across all industries and business functions, and extensive research on the world\u2019s most successful companies, Accenture collaborates with clients to help them become high-performance businesses and governments. The company generated net revenues of US$21.6 billion for the fiscal year ended Aug. 31, 2010.\r\n\r\nAccenture inviterer til bedriftspresentasjon for siv.ing Fysikk og Matematikk klokken 17:15 i R8 p\xe5 realfagsbygget.\r\n\r\nBespisning: Asiatisk buffet p\xe5 Kos', u'is_advertised': u'1', u'title': u'Accenture', u'registration_start': u'2012-02-20 12:00:00', u'seats_available': 0, u'seats': u'15', u'min_year': u'3', u'open_for': u'3', u'place': u'R8', u'registration_started': u'1', u'web_page': u'http://www.accenture.com/us-en/pages/index.aspx', u'time': u'2012-03-01 17:15:00', u'deadline_passed': u'0', u'deadline': u'2012-02-29 12:00:00', u'max_year': u'5', u'id': u'325', u'logo': u'http://bpc.timini.no/logo/bedpres.png', u'this_attending': u'15'}, {u'count_waiting': 0, u'description_formatted': u'<p>Det legges ut 14 ekstra plasser til presentasjonen p\xe5 torsdag. Disse plassene er \xe5pne for b\xe5de Timini og Nabla.</p>\n\n<p><strong>NB!</strong> Ikke meld deg p\xe5 her hvis du allerede har f\xe5tt plass.</p>\n', u'waitlist_enabled': u'1', u'description': u'Det legges ut 14 ekstra plasser til presentasjonen p\xe5 torsdag. Disse plassene er \xe5pne for b\xe5de Timini og Nabla.\r\n\r\n**NB!** Ikke meld deg p\xe5 her hvis du allerede har f\xe5tt plass.', u'is_advertised': u'1', u'title': u'Accenture - ekstra plasser', u'registration_start': u'2012-02-28 12:00:00', u'seats_available': 14, u'seats': u'14', u'min_year': u'3', u'open_for': u'3', u'place': u'R8', u'registration_started': u'0', u'web_page': u'http://www.accenture.com', u'time': u'2012-03-01 17:15:00', u'deadline_passed': u'0', u'deadline': u'2012-02-29 19:00:00', u'max_year': u'5', u'id': u'364', u'logo': u'http://bpc.timini.no/logo/accenture_logo-1203695520961.png', u'this_attending': u'0'}]}
#{u'error': [{u'403': u'Error: No events.<br />'}]}
