from __future__ import unicode_literals

from collections import OrderedDict

from django.utils import timezone

from .settings import IMPORT_FROM, LIMIT_PREVIEW, FILE_PATH
from .models import Report


class ProcessorExists(Exception):
    pass


class Processor(object):
    """Base implementation of import and export operations"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, filepath, settings, queryset):
        self.filepath = filepath
        self.settings = settings
        self.queryset = queryset

    def prepare(self):
        pass

    def col_index(self, value):
        """Return column index for given name"""

        raise NotImplementedError

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value):
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

        report = Report.objects.create(action=Report.EXPORT)

        self.prepare()

        # using with template and xlutils.copy (not tested python3)
        # openpyxl don't allow to write in single cell :( so we need to copy
        # row from original xlsx file and replace values from new row
        # implement this in write methood for openpyxl
        # start, end = self.dimensions(0, 0, worksheet.nrows, worksheet.ncols)
        start, end = self.dimensions(0, 0, data['rows'], data['cols'])

        if self.settings.include_header:
            header_data = map(lambda f: f.name, self.settings.fields.all())

            self.write(
                start['row'], header_data, range(start['col'], end['col']))

            start['row'] += 1
            end['row'] += 1

        for rindex, row in enumerate(range(start['row'], end['row'])):
            row_data = []
            for cindex, col in enumerate(range(start['col'], end['col'])):
                row_data.append(next(data['items']))
            self.write(row, row_data)

        # save external file and report
        path = FILE_PATH()(report, str(report.id))
        self.save(path)

        print path

        report.buffer_file = path
        report.completed_at = timezone.now()
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
            raise ProcessorExists('Processor already exists')
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

    def import_processors(self):
        """Import modules within IMPORT_FROM paths"""

        for module in IMPORT_FROM():
            try:
                __import__(module)
            except ImportError:
                print('Invalid module {}, unable to import'.format(module))

manager = Manager.create()
