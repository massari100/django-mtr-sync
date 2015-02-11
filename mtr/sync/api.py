from __future__ import unicode_literals

import os

from collections import OrderedDict

from django.utils.six.moves import range
from django.utils import timezone

from .settings import IMPORT_FROM, LIMIT_PREVIEW, FILE_PATH
from .models import Report


class ProcessorDoesNotExists(Exception):
    pass

class ProcessorAlreadyExists(Exception):
    pass


class Processor(object):
    """Base implementation of import and export operations"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings):
        self.settings = settings

    def prepare(self):
        pass

    def col(self, value):
        """Return column index for given name"""

        raise NotImplementedError

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def dimensions(
            self, start_row, start_col, end_row, end_col, preview=False):
        """Return start, end table dimensions"""

        start = {'row': start_row, 'col': start_col}
        end = {'row': end_row, 'col': end_col}

        if self.settings.limit_data:
            if self.settings.start_row >= start_row:
                start['row'] = self.settings.start_row
            if self.settings.end_row <= end_row:
                end['row'] = self.settings.end_row

        limit = LIMIT_PREVIEW()
        if preview and limit <= end_row:
            end_row = limit

        if self.settings.limit_data:
            start_col_index = self.col(self.settings.start_col)
            end_col_index = self.col(self.settings.end_col)

            if start_col_index >= start_col:
                start['col'] = start_col_index
            if end_col_index <= end_col:
                end['col'] = end_col_index

        return (start, end)

    def export_data(self, data):
        """Export data from queryset to file and return path"""

        report = Report.export_objects.create(action=Report.EXPORT)

        self.create()

        start, end = self.dimensions(0, 0, data['rows'], data['cols'])

        if self.settings.include_header and self.settings.fields.all():
            header_data = map(lambda f: f.name, self.settings.fields.all())

            self.write(
                start['row'], header_data, range(start['col'], end['col']))

            start['row'] += 1
            end['row'] += 1

        cells = range(start['col'], end['col'])
        for rindex, row in enumerate(range(start['row'], end['row'])):
            row_data = []
            for cindex, col in enumerate(cells):
                row_data.append(next(data['items']))
            self.write(row, row_data, cells)

        # save external file and report
        path = FILE_PATH()(report, '')
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(
            path, '{}{}'.format(str(report.id), self.file_format))
        self.save(path)

        report.completed_at = timezone.now()
        report.status = Report.SUCCESS
        report.buffer_file = path
        report.save()

        return report

    # def import_data(self):
    #     """Import data to model and return errors if exists"""

    #     raise NotImplementedError


class Manager(object):
    """Manager for data processors"""

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
            raise ProcessorAlreadyExists(
                'Processor {} already exists'.format(cls.__name__))
        self.processors[cls.__name__] = cls

        if cls.position:
            self.processors = OrderedDict(
                sorted(self.processors.items(), key=lambda p: p.position))

        return cls

    def unregister(self, cls):
        """Decorator to pop processor"""

        self.processors.pop(cls.__name__, None)

        return cls

    def has_processor(self, cls):
        """Check if processor already exists"""

        return True if self.processors.get(cls.__name__, False) else False

    def make_processor(self, settings):
        """Create new processor instance if exists"""

        processor = self.processors.get(settings.processor, None)

        if processor is None:
            raise ProcessorDoesNotExists(
                'Processor {} does not exists'.format(settings.processor))

        return processor(settings)

    def export_data(self, settings, data):
        """Raw data export"""

        processor = self.make_processor(settings)

        return processor.export_data(data)

    def prepare_data(self, settings):
        """Prepare data using filters and settings"""
        pass

    def import_processors(self):
        """Import modules within IMPORT_FROM paths"""

        for module in IMPORT_FROM():
            try:
                __import__(module)
            except ImportError:
                print('Invalid module {}, unable to import'.format(module))

manager = Manager.create()
