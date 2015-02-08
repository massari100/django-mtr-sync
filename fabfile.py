import os

from fabric.api import local, task, settings, hide, lcd

APPS = ['mtr.sync']
PROJECT_DIR = 'tests'


@task
def clear():
    """Delete unnecessary and cached files"""

    local("find . -name '~*' -or -name '*.pyo' -or -name '*.pyc' "
        "-or -name 'Thubms.db' | xargs -I {} rm -v '{}'")


@task
def test():
    """Test listed apps"""

    with settings(hide('warnings'), warn_only=True):
        test_apps = ' '.join(map(lambda app: '{}.tests'.format(app), APPS))
        with lcd(PROJECT_DIR):
            local("./manage.py test {} --pattern='*.py'".format(test_apps))


@task
def run():
    """Run server"""

    with lcd(PROJECT_DIR):
        local('./manage.py runserver')


@task
def celery():
    """Start celery worker"""

    with lcd(PROJECT_DIR):
        local('celery worker -A app')


@task
def locale(action='make', lang='en'):
    """Make messages, and compile messages for listed apps"""

    if action == 'make':
        for app in APPS:
            with lcd(os.path.join(*app.split('.'))):
                local('django-admin.py makemessages -l {}'.format(lang))
    elif action == 'compile':
        for app in APPS:
            with lcd(os.path.join(*app.split('.'))):
                local('django-admin.py compilemessages -l {}'.format(lang))
    else:
        print('Invalid action: {}, available actions: "make"'
            ', "compile"'.format(action))


@task
def install():
    """Install packages for testing"""

    with lcd(PROJECT_DIR):
        local('pip install -r requirements.txt')
