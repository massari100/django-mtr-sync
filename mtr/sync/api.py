from __future__ import unicode_literals

from collections import OrderedDict

from .settings import IMPORT_FROM


class ProcessorExists(Exception):
    pass


class Processor(object):
    """Base implementation of import and export operations"""

    formats = OrderedDict()

    def __init__(self, filepath, settings):
        self.filepath = filepath
        self.settings = settings

    def export_data(self, queryset):
        """Export data from queryset to file and return path"""

        raise NotImplementedError

    def import_data(self, data, model):
        """Import data to model and return errors if exists"""

        raise NotImplementedError


class Manager(object):
    """Manager for registering new processors"""

    def __init__(self):
        self.processors = OrderedDict()

    @classmethod
    def create(cls):
        """Create api manager and import processors"""

        manager = cls()
        manager.import_processors()
        return manager

    def register(self, cls):
        """Decorator to append new processor"""

        if self.has_processor(cls):
            raise ProcessorExists('Processor already exists')
        self.processors[cls.__name__] = cls

        return cls

    def unregister(self, cls):
        """Decorator to pop processor"""

        self.processors.pop(cls.__name__, None)

        return cls

    def has_processor(self, cls):
        """Check if processor already exists"""

        return True if self.processors.get(cls.__name__, False) else False

    def import_processors(self):
        """Import modules within IMPORT_FROM paths"""

        for module in IMPORT_FROM():
            try:
                __import__(module)
            except ImportError:
                print('Invalid module {}, unable to import'.format(module))

manager = Manager.create()
