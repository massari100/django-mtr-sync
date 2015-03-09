import os

from fabric.api import local, task, lcd

APPS = ['mtr.sync']
PROJECT_APPS = ['app']
PROJECT_DIR = 'tests'
DOCS_DIR = 'docs'


@task
def clear():
    """Delete unnecessary and cached files"""

    local("find . -name '~*' -or -name '*.pyo' -or -name '*.pyc' "
        "-or -name '__pycache__' -or -name 'Thubms.db' "
        "| xargs -I {} rm -vrf '{}'")


@task
def manage(command, prefix=None, nocd=False):
    """Shortcut for manage.py file"""

    run = '{}/manage.py {{}}'.format(PROJECT_DIR if nocd else '.')

    if prefix:
        run = '{} {}'.format(prefix, run)

    if nocd:
        local(run.format(command))
    else:
        with lcd(PROJECT_DIR):
            local(run.format(command))


@task
def test(coverage=False):
    """Test listed apps"""

    apps = []
    apps.extend(PROJECT_APPS)
    apps.extend(APPS)
    test_apps = ' '.join(map(lambda app: '{}.tests'.format(app), apps))
    command = "test {} --pattern='*.py'".format(test_apps)

    if coverage:
        coverage = "coverage run --omit=*.virtualenvs/*," \
            "*migrations/*.py,*tests*,*/admin.py"

    manage(command, prefix=coverage, nocd=coverage)


@task
def run():
    """Run server"""

    manage('runserver')


@task
def shell():
    """Start interactive shell"""

    manage('shell')


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


@task
def migrate():
    """Make migrations and migrate"""

    manage('makemigrations')
    manage('migrate')


@task
def recreate():
    """Recreate new migrations from start and remove database"""

    for app in APPS:
        with lcd(os.path.join(*app.split('.'))):
            local('rm -f ./migrations/*.py')
            local('touch ./migrations/__init__.py')
    with lcd(PROJECT_DIR):
        local('rm -f *.sqlite3')

    migrate()

    manage('createsuperuser --username app --email app@app.com --noinput')
    manage('changepassword app')


@task
def subl():
    """Start Sublime editor"""

    local('subl project.sublime-workspace')


@task
def docs(action='make'):
    """Sphinx docs generation"""

    with lcd(DOCS_DIR):
        if action == 'make':
            local('make html')
        else:
            print('Invalid action: {}, available actions: "make"'
                ', "compile"'.format(action))
