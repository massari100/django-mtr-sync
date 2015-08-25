from collections import OrderedDict


class Manager(object):

    """Manager for different kind of functions"""

    def __init__(self):
        self._registered = {}
        self._imported = False

    def get(self, type_name, func_name, inner=None):
        funcs = self._registered.get(type_name, {})
        if inner and funcs:
            funcs = funcs.get(inner, {})
        return funcs.get(func_name, None)

    def _register_dict(
            self, type_name, func_name, label, inner=None, **kwargs):
        """Return decorator for adding functions as key, value
        to instance, dict"""

        def decorator(func):
            key = type_name
            outer = None
            values = self._registered.get(key, OrderedDict())
            if inner:
                outer = values
                values = values.get(inner, OrderedDict())
            position = \
                getattr(func, 'position', 0) or kwargs.get('position', 0)
            new_name = func_name or func.__name__

            if values.get(new_name, None) is not None:
                raise ValueError(
                    '{} already registred at {}'.format(new_name, key))

            values[new_name] = func
            if position:
                values = OrderedDict(
                    sorted(
                        values.items(),
                        key=lambda p: getattr(p[1], 'position', 0)))
            if inner and outer:
                outer[key] = inner
                values = outer
            self._registered[key] = values

            return func

        return decorator

    def register(
            self, type_name, label=None, name=None,
            item=None, inner=None, **kwargs):
        """Decorator and function to config new handlers"""

        func = self._register_dict(type_name, name, label, **kwargs)

        return func(item) if item else func

    def unregister(self, type_name, item=None, inner=None):
        """Decorator to pop dict items"""

        items = self._registered.get(type_name, None)
        if items is not None:
            items.pop(getattr(item, '__name__', item), None)

        return item

    def import_modules(self, modules):
        """Import modules within aditional paths"""

        if not self.imported:
            for module in modules:
                try:
                    __import__(module)
                except:
                    pass

            self.imported = True


class TemplateContextManager(Manager):
    pass
