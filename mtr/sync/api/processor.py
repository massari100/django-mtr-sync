from __future__ import unicode_literals

import os

from django.utils.six.moves import range
from django.utils import timezone

from .signals import export_started, export_completed, \
    import_started, import_completed
from ..settings import LIMIT_PREVIEW, FILE_PATH


class Processor(object):
    """Base implementation of import and export operations"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings, manager):
        self.settings = settings
        self.manager = manager
        self.report = None

    def column_index(self, value):
        """Return column index for given name"""

        raise NotImplementedError

    def column(self, value):
        """Wrapper on self.column"""

        if isinstance(value, int):
            return value

        if value.isdigit():
            return int(value)

        return self.column_index(value)

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def set_dimensions(
            self, start_row, start_col, end_row, end_col, preview=False,
            import_data=False):
        """Return start, end table dimensions"""

        start = {'row': start_row, 'col': start_col}
        end = {'row': end_row, 'col': end_col}

        if self.settings.start_row and \
                self.settings.start_row > start_row:
            start['row'] = self.settings.start_row - 1
            end['row'] += start['row']

        if self.settings.end_row and \
                self.settings.end_row < end['row']:
            end['row'] = self.settings.end_row

        limit = LIMIT_PREVIEW()
        if preview and limit < end_row:
            end_row = limit

        if self.settings.start_col:
            start_col_index = self.column(self.settings.start_col)
            if start_col_index > start_col:
                start['col'] = start_col_index - 1

                if not import_data:
                    end['col'] += start['col']

        if self.settings.end_col:
            end_col_index = self.column(self.settings.end_col)

            if end_col_index < end['col']:
                end['col'] = end_col_index

        if self.settings.include_header and import_data:
            start['row'] += 1

        if import_data:
            end['row'] -= 1

        self.start, self.end = start, end
        self.cells = range(start['col'], end['col'])
        self.rows = range(start['row'], end['row'])

        return (start, end)

    def export_data(self, data):
        """Export data from queryset to file and return path"""

        # send signal to create report
        for response in export_started.send(self.__class__, processor=self):
            self.report = response[1]

        self.set_dimensions(0, 0, data['rows'], data['cols'])

        # create export file for write
        self.create()

        # write header
        if self.settings.include_header and data['fields']:
            header_data = map(
                lambda f: f.name or f.attribute,
                data['fields'])

            self.write(self.start['row'], header_data)

            self.start['row'] += 1
            self.end['row'] += 1

            self.rows = range(self.start['row'], self.end['row'])

        # write data
        data = data['items']
        for row in self.rows:
            row_data = []

            for col in self.cells:
                row_data.append(next(data))

            self.write(row, row_data)

        # save external file and report
        path = FILE_PATH()(self.report, '')
        if not os.path.exists(path):
            os.makedirs(path)

        filename = '{}{}'.format(
            self.settings.filename or str(self.report.id), self.file_format)

        path = os.path.join(path, filename)
        self.save(path)

        if self.settings.id:
            self.report.settings = self.settings

        # send signal to save report
        for response in export_completed.send(
                self.__class__, report=self.report,
                date=timezone.now(),
                path=FILE_PATH()(self.report, filename, relative=True)):
            self.report = response[1]

        return self.report

    def import_data(self, model, path=None):
        """Import data to model and return errors if exists"""

        path = path or self.settings.buffer_file.path

        # send signal to create report
        for response in import_started.send(self.__class__, processor=self,
                path=path):
            self.report = response[1]

        # open file and set dimensions
        max_rows, max_cols = self.open(path)
        self.set_dimensions(0, 0, max_rows, max_cols, import_data=True)

        # TODO: transaction management
        # TODO: update if, create if, delete if

        rows = (self.read(row) for row in self.rows)
        data = self.manager.prepare_import_data(self, rows)

        # models_to_create = []
        for attr in data:
            # models_to_create(model(**data))
            model.objects.create(**attr)

            # TODO: bulk create or with save
        # model.objects.bulk_create(models_to_create)

        if self.settings.id:
            self.report.settings = self.settings

        # send signal to save report
        for response in import_completed.send(
                self.__class__, report=self.report,
                date=timezone.now()):
            self.report = response[1]

        return self.report
