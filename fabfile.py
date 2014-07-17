
import os

from fabric.api import cd, env, execute, local, run, task
from fabric.colors import green, red


CONFIG = {
    'venv': 'venv',
    'python_version': 'python2.7',
    'project': 'nablaweb',
}

CONFIG['django_manage'] = '{venv}/bin/python {project}/manage.py'.format(**CONFIG)


def setup_dev():
    setup_virtualenv()
    pip_install_requirements()
    local('mkdir var')
    setup_database()
    collect_static()


def setup_virtualenv():
    if os.path.exists(CONFIG['venv']):
        print(red('Det ser ut som om virtualenv allerede er satt opp.'))
        return 1
    local('virtualenv --python={python_version} {venv}'.format(**CONFIG))


def pip_install_requirements(requirements="requirements/devel.txt"):
    local('{venv}/bin/pip install -r {requirements}'.format(requirements=requirements, **CONFIG))


def setup_database():
    local('{django_manage} syncdb'.format(**CONFIG))
    local('{django_manage} migrate'.format(**CONFIG))


def collect_static():
    local('{django_manage} collectstatic'.format(**CONFIG))


def runserver(port=8000):
    local('{django_manage} runserver 0.0.0.0:{port}'.format(port=port, **CONFIG))
