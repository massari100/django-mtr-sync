import xlrd
import xlwt

from django.utils.translation import gettext_lazy as _

from ..processor import Processor
from ..manager import manager


@manager.register
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('mtr.sync:Microsoft Excel 97/2000/XP/2003')

    def col(self, value):
        """Small xlrd hack to get column index"""

        if value.isdigit():
            return int(value)

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

    def write(self, row, value):
        for index, cell in enumerate(self.cells):
            self._worksheet.write(row, cell, value[index])

    def read(self, row):
        for index, cell in enumerate(self.cells):
            yield self._worksheet.cell_value(row, cell)

    def save(self, name):
        self._workbook.save(name)
