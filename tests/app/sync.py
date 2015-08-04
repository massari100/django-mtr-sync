from mtr.sync.lib.manager import manager


@manager.register('dataset', label='some description')
def some_dataset(model, settings):
    return model.objects.filter(security_level__gte=30)


@manager.register('settings', model='app.Person')
def person_settings(model):
    return {
        'custom_fields': ['custom_method', 'none_param'],
        'exclude': ['some_excluded_field']
    }
