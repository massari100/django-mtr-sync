import openpyxl

from django.utils.translation import gettext_lazy as _

from ..processor import Processor
from ..manager import manager


@manager.register
class XlsxProcessor(Processor):
    file_format = '.xlsx'
    file_description = _('mtr.sync:Microsoft Excel 2007/2010/2013 XML')

    def column_index(self, value):
        return openpyxl.cell.column_index_from_string(value)

    def create(self):
        self._workbook = openpyxl.Workbook(optimized_write=True)
        self._worksheet = self._workbook.create_sheet()
        self._worksheet.name = self.settings.worksheet
        self._prepend = None

        # prepend rows and cols
        if self.start['row'] > 0:
            for i in range(0, self.start['row']):
                self._worksheet.append([])

        if self.start['col'] > 0:
            self._prepend = [None, ]
            self._prepend *= self.start['col']

    def open(self):
        self._workbook = openpyxl.open_workbook(self.settings.buffer_file)
        self._worksheet = self._workbook(self.settings.worksheet)

    def write(self, row, value):
        # if we have cells we need to copy from templated file all row
        # and merge cells into

        if self._prepend:
            value = self._prepend + value

        self._worksheet.append(value[:self.end['col']])

    def read(self, row, cells):
        # using optimized reader
        # for index, cell in enumerate(cells):
        #     yield self._worksheet.cell_value(row, cell)
        pass

    def save(self, name):
        self._workbook.save(name)
