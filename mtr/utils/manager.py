from collections import OrderedDict


class Manager(object):

    """Manager for data processors"""

    def __init__(self):
        self.processors = OrderedDict()
        self.actions = OrderedDict()
        self.converters = OrderedDict()
        self.datasets = OrderedDict()
        self.befores = OrderedDict()
        self.afters = OrderedDict()
        self.errors = OrderedDict()

        self.imported = False

    def _make_key(self, key):
        return '{}s'.format(key)

    def get_or_raise(self, name, key):
        # TODO: remove method

        value = getattr(self, self._make_key(name), {})
        value = value.get(key, None)

        if value is None:
            raise ValueError(
                '{} not registered at {}'.format(key, name))

        return value

    def has(self, name, key):
        for value in getattr(self, self._make_key(name), {}).values():
            if value == key:
                return True
        return False

    def _register_dict(self, type_name, func_name, label, **kwargs):
        """Return decorator for adding functions as key, value
        to instance, dict"""

        def decorator(func):
            key = self._make_key(type_name)
            values = getattr(self, key, OrderedDict())
            position = getattr(func, 'position', 0)
            new_name = func_name or func.__name__

            func.label = label
            func.use_transaction = kwargs.get('use_transaction', False)

            if values is not None:
                if values.get(new_name, None) is not None:
                    raise ValueError(
                        '{} already registred at {}'.format(new_name, key))

                values[new_name] = func
                if position:
                    values = OrderedDict(
                        sorted(
                            values.items(),
                            key=lambda p: getattr(p[1], 'position', 0)))
                setattr(self, key, values)

            return func

        return decorator

    def register(self, type_name, label=None, name=None, item=None, **kwargs):
        """Decorator and function to config new processors, handlers"""

        func = self._register_dict(type_name, name, label, **kwargs)

        return func(item) if item else func

    def unregister(self, type_name, item=None):
        """Decorator to pop dict items"""

        items = getattr(self, self._make_key(type_name), None)
        if items is not None:
            items.pop(getattr(item, '__name__', item), None)

        return item

    def import_module(self, modules):
        """Import modules within aditional paths"""

        if not self.imported:
            for module in modules:
                try:
                    __import__(module)
                except:
                    pass

            self.imported = True
