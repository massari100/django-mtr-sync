from __future__ import unicode_literals

import os

from django.utils.six.moves import range
from django.utils import timezone

from .signals import export_started, export_completed
from ..settings import LIMIT_PREVIEW, FILE_PATH


class Processor(object):
    """Base implementation of import and export operations"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings):
        self.settings = settings
        self.report = None

    def col(self, value):
        """Return column index for given name"""

        raise NotImplementedError

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def set_dimensions(
            self, start_row, start_col, end_row, end_col, preview=False):
        """Return start, end table dimensions"""

        start = {'row': start_row, 'col': start_col}
        end = {'row': end_row, 'col': end_col}

        if self.settings.start_row and \
                self.settings.start_row >= start_row:
            start['row'] = self.settings.start_row - 1
            end['row'] += start['row']

        if self.settings.end_row and \
                self.settings.end_row <= end['row']:
            end['row'] = self.settings.end_row

        limit = LIMIT_PREVIEW()
        if preview and limit <= end_row:
            end_row = limit

        if self.settings.start_col:
            start_col_index = self.col(self.settings.start_col)

            if start_col_index >= start_col:
                start['col'] = start_col_index - 1
                end['col'] += start['col']

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
        if self.settings.include_header and self.settings.fields.all():
            header_data = map(
                lambda f: f.name or f.attribute,
                self.settings.fields.all())

            self.write(self.start['row'], header_data)

            self.start['row'] += 1
            if self.settings.end_row:
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

    # def import_data(self):
    #     """Import data to model and return errors if exists"""

    #     raise NotImplementedError
