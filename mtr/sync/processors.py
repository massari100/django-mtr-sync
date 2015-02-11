from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from .api import Processor, manager

try:
    import xlrd
    import xlwt
except ImportError:
    pass


@manager.register
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('Microsoft Excel 97/2000/XP/2003')

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
            yield self._worksheet.cell(row, cell)

    def save(self, name):
        self._workbook.save(name)


# class XlsxProcessor(Processor):
#     data_type = 'table'


# class OdsProcessor(Processor):
#     data_type = 'table'
