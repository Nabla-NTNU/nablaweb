# -*- coding: utf-8 -*-


import re
from urllib import urlencode
from urllib2 import urlopen, Request, URLError
from datetime import datetime
from phpserialize.phpserialize import unserialize


# Samleunntak.
class BPCException(Exception):
    def __init__(self, message):
        super(BPCException, self).__init__(message)

# Unntak som skyldes feil generert her.
class BPCClientException(BPCException):
    def __init__(self, message):
        super(BPCClientException, self).__init__(message)

# Feil som rapporteres av BPC.
class BPCResponseException(BPCException):
    def __init__(self, message):
        super(BPCResponseException, self).__init__(message)


BPC_URL = 'https://bpc.timini.no/bpc_testing/remote/'
BPC_URL = 'https://bpc.timini.no/bpc/remote/'


SETTINGS = {
    'forening': '3',
    'key': 'a88fb706bc435dba835b89ddb2ba4debacc3afe4',
#    'key': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'method': 'serialized_array',
    'debug': 'false',
    'timing': 'false',
    'version': '1.1',
    }


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
    }


# RESPONSES = {
#     'get_events':
#         {'event':
#              {'required': ('id', 'title', 'description', 'time', 'place', 'web_page', 'logo', 'deadline', 'deadline_passed', 'is_advertised', 'registration_start', 'registration_started', 'seats', 'seats_available', 'this_attending', 'open_for', 'waitlist_enabled', 'count_waiting', 'web_page'),
#               'optional': ('is_waiting', 'attending')}}
#
#     'add_attending':
#         {'add_attending':
#              {'required': (),
#               'optional': ('waiting',)}}
#
#     'rem_attending':
#         {'rem_attending':
#              {'required': (),
#               'optional': ()}}
#
#     'get_attending':
#         {'users':
#              {'required': ('user_id', 'fullname', 'username', 'reigstered', 'year'),
#               'optional': ()}}
#
#     'get_waiting':
#         {'users':
#              {'required': ('user_id', 'fullname', 'username', 'reigstered', 'year'),
#               'optional': ()}}
#
#     'get_user_stats':
#         {'event':
#              {'required': ('id', 'title', 'time', 'is_advertised', 'attended', 'on_waitlist'),
#               'optional': ()}
#          'user_stats':
#              {'required': ('events', 'attended', 'on_waitlist'),
#               'optional': ()}
#          }
#     }


BPC_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


BPC_ERRORS = {
    # Fatalt - Disse avbryter skriptet.
    '101': 'Feil eller ingen handshake',
    '102': 'Feil eller ingen request',
    '103': 'Ingen eller ikke-eksisterende event',
    '104': 'Feil i SQL-spørring',
    '105': 'Feil eller ikke noe brukernavn gitt',
    '106': 'Feil eller ikke noe fullstendig navn gitt',
    '107': 'Feil eller ikke noe kortnummer gitt',

    # Feil - Alvorlige feil som ikke bør skje med en korrekt oppsatt
    # klient, men ikke så alvorlige at skriptet avbrytes. En fatal
    # feil vil ofte følge etter en vanlig feil, disse kan da hjelpe
    # til å spore problemet.
    '201': 'Feil i validering av en parameter',
    '202': 'Du har ikke tilgang til å gjøre dette',
    '203': 'PHP-feil i scriptet på serveren',

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
def _create_valid_request(data):
    request = SETTINGS.copy()

    def _copy_parameters(parameters, raise_error, error_msg):
        for parameter in parameters:
            try:
                request[parameter] = data[parameter]
                _validate_parameter(parameter, data[parameter])
            except KeyError:
                if raise_error:
                    raise BPCClientException(error_msg % parameter)

    _copy_parameters(['request'], raise_error=True, error_msg="Parameter '%s' is required.")
    _copy_parameters(REQUESTS[request['request']]['required'], raise_error=True, error_msg="Parameter '%s' is required for request type '%s'." % ('%s', request['request']))
    _copy_parameters(REQUESTS[request['request']]['optional'], raise_error=False, error_msg=None)

    return request


def make_request(data):
    # TODO: Sjekk hvilke unntak som risikeres fra urlencode og urlopen.

    request = _create_valid_request(data)
    request = Request(BPC_URL, urlencode(request))

    try:
        fd = urlopen(request)
        raw_data = fd.read()
        fd.close()
    except URLError:
        raise BPCClientException("Could not contact server.")

    return unserialize(raw_data)


def convert_names(bpc_info):
    key_map = {
        'count_waiting': 'count_waiting',
        'waitlist_enabled': 'has_queue',
        'description': 'description',
        'is_advertised': 'is_advertised',
        'title': 'headline',
        'registration_start': 'registration_start',
        'seats_available': 'seats_available',
        'seats': 'places',
        'min_year': 'min_year',
        'open_for': 'open_for',
        'deadline': 'registration_deadline',
        'registration_started': 'registration_started',
        'web_page': 'web_page',
        'time': 'event_start',
        'deadline_passed': 'deadline_passed',
        'place': 'location',
        'max_year': 'max_year',
        'id': 'bpcid',
        'logo': 'logo',
        'this_attending': 'this_attending',
        }
    # TODO: Ta høyde for KeyError.
    return dict((key_map[key], value) for (key, value) in bpc_info.iteritems())


def convert_types(bpc_info):
    type_map = {
        'count_waiting': int,
        'has_queue': lambda x: bool(int(x)),
        'description': str,
        'is_advertised': lambda x: bool(int(x)),
        'headline': str,
        'registration_start': lambda x: datetime.strptime(x, BPC_TIME_FORMAT),
        'seats_available': int,
        'places': int,
        'min_year': int,
        'open_for': int,
        'registration_deadline': lambda x: datetime.strptime(x, BPC_TIME_FORMAT),
        'registration_started': lambda x: bool(int(x)),
        'web_page': str,
        'event_start': lambda x: datetime.strptime(x, BPC_TIME_FORMAT),
        'deadline_passed': lambda x: bool(int(x)),
        'location': str,
        'max_year': int,
        'bpcid': str,
        'logo': str,
        'this_attending': int,
        }
    return dict((key, type_map[key](value)) for (key, value) in  bpc_info.iteritems())

def get_single_event(bedpres_id):
    bpc_dict = make_request({'request': 'get_events',
                               'event': bedpres_id})
    event = bpc_dict.get('event')
    if event is None:
        raise BPCException(BPC_ERRORS['403'])
    event = event.get(0)
    return convert_types(convert_names(event))


def get_future_events():
    bpc_dict = make_request({'request': 'get_events'})
    events = bpc_dict.get('event')
    if events is None:
        raise BPCException(BPC_ERRORS['403'])
    event_list = []
    # TODO: Sorter på dato eller noe.
    # TODO: Sjekk om de allerede er sortert på noe.
    for number, event_info in events.iteritems():
        event_list.append(convert_types(convert_names(event_info)))
    return event_list

# {'has_queue': '0',
#  'registration_deadline': '2011-10-31 12:00:00',
#  'this_attending': '5',
#  'is_advertised': '1',
#  'count_waiting': '0',
#  'seats_available': 20,
#  'title': 'Baker Hughes',
#  'event_start': '2011-10-31 17:15:00',
#  'summary': 'A top-tier oilfield service company with a century-long track record, Baker Hughes delivers solutions that help oil and gas operators make the most of their reservoirs.',
#  'min_year': '1',
#  'open_for': '1',
#  'registration_start': '2011-10-27 17:00:00',
#  'registration_started': '1',
#  'web_page': 'http://www.bakerhughes.com/',
#  'seats': '25',
#  'deadline_passed': '0',
#  'logo': 'http://bpc.timini.no/logo/bedpres.png',
#  'max_year': '5',
#  'bpcid': '305',
#  'location': 'PTS'}
