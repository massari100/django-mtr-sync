import xlrd
import xlwt

from django.utils.translation import gettext_lazy as _

from ..processor import Processor
from ..manager import manager


class NoIndexFound(Exception):
    pass


@manager.register('processor')
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('mtr.sync:Microsoft Excel 97/2000/XP/2003')

    def column_index(self, value):
        """Small xlrd hack to get column index"""

        index = 0
        value = value.strip().upper()

        while True:
            if xlrd.colname(index) == value:
                return index - 1
            index += 1
            if index > 16384:
                raise NoIndexFound

    def create(self):
        self._workbook = xlwt.Workbook('utf-8')
        self._worksheet = self._workbook.add_sheet(self.settings.worksheet)

    def open(self, path):
        self._workbook = xlrd.open_workbook(path)
        self._worksheet = self._workbook.sheet_by_name(
            self.settings.worksheet)

        return self._worksheet.nrows, self._worksheet.ncols

    def write(self, row, value):
        for index, cell in enumerate(self.cells):
            self._worksheet.write(row, cell, value[index])

    def read(self, row):
        data = []
        for cell in self.cells:
            data.append(self._worksheet.cell_value(row, cell))
        return data

    def save(self, name):
        self._workbook.save(name)
