from fabric.api import local, task, settings, hide

APPS = ['mtr.sync']


@task
def clear():
    """Delete unnecessary and cached files"""

    local("find . -name '~*'' -or -name '*.pyo' -or -name '*.pyc' "
        "-or -name 'Thubms.db' | xargs -I {} rm -v '{}'")


@task
def test():
    """Test listed apps"""

    with settings(hide('warnings'), warn_only=True):
        test_apps = ' '.join(map(lambda app: '{}.tests'.format(app), APPS))
        local("./manage.py test {} --pattern='*.py'".format(test_apps))


@task
def run():
    """Run server"""

    local("./manage.py runserver")
