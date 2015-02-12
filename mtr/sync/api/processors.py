from __future__ import unicode_literals

import os

from django.utils.translation import gettext_lazy as _
from django.utils.six.moves import range
from django.utils import timezone

from .manager import manager
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

        for response in export_started.send(self.__class__, processor=self):
            self.report = response[1]

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
        path = FILE_PATH()(self.report, '')
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(
            path, '{}{}'.format(str(self.report.id), self.file_format))
        self.save(path)

        for response in export_completed.send(
                self.__class__, report=self.report,
                date=timezone.now(), path=path):
            self.report = response[1]

        return self.report

    # def import_data(self):
    #     """Import data to model and return errors if exists"""

    #     raise NotImplementedError

# TODO: default import configuration, import dependencies

try:
    import xlrd
    import xlwt
except ImportError:
    pass


@manager.register
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('mtr.sync:Microsoft Excel 97/2000/XP/2003')

    def col(self, value):
        """Small xlrd hack to get column index"""

        index = 0
        value = value.strip().upper()
        while index:
            if xlrd.colname(index) == value:
                return index

    def create(self):
        self._workbook = xlwt.Workbook('utf-8')
        self._worksheet = self._workbook.add_sheet(self.settings.worksheet)

    def open(self):
        self._workbook = xlrd.open_workbook(self.settings.buffer_file)
        self._worksheet = self._workbook(self.settings.worksheet)

    def write(self, row, value, cells=None):
        for index, cell in enumerate(cells):
            self._worksheet.write(row, cell, value[index])

    def read(self, row, cells=None):
        for index, cell in enumerate(cells):
            yield self._worksheet.cell_value(row, cell)

    def save(self, name):
        self._workbook.save(name)


# class XlsxProcessor(Processor):
#     data_type = 'table'


# class OdsProcessor(Processor):
#     data_type = 'table'
