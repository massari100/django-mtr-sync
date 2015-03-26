from .manager import manager


@manager.register('valueprocessor', label='mtr.sync:Auto')
def auto(value, field, action):
    print(field)
    return action, value
