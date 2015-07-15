import django


if django.get_version() >= '1.7':
    from mtr.sync.api import manager
else:
    from mtr_sync.api import manager


@manager.register('dataset', label='some description')
def some_dataset(model, settings):
    return model.objects.filter(security_level__gte=30)
