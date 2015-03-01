import os

os.environ['OPENPYXL_LXML'] = 'False'

import openpyxl

from django.utils.translation import gettext_lazy as _

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class XlsxProcessor(Processor):
    file_format = '.xlsx'
    file_description = _('mtr.sync:Microsoft Excel 2007/2010/2013 XML')

    def create(self, path):
        self._path = path
        self._prepend = None
        self._workbook = openpyxl.Workbook(optimized_write=True)
        self._worksheet = self._workbook.create_sheet()
        self._worksheet.title = self.settings.worksheet

        # prepend rows and cols
        if self.start['row'] > 1:
            for i in range(0, self.start['row']):
                self._worksheet.append([])

        if self.start['col'] > 1:
            self._prepend = [None, ]
            self._prepend *= self.start['col']

    def open(self, path):
        self._workbook = openpyxl.load_workbook(path, use_iterators=True)

        if not self.settings.worksheet:
            self.settings.worksheet = self._workbook.get_sheet_names()[0]

        self._worksheet = self._workbook.get_sheet_by_name(
            self.settings.worksheet)

        self._rows = self._worksheet.iter_rows()
        self._rows_counter = 0

        return (
            self._worksheet.get_highest_row(),
            self._worksheet.get_highest_column())

    def write(self, row, value):
        if self._prepend:
            value = self._prepend + value

        self._worksheet.append(value[:self.end['col']])

    def read(self, row):
        value = None
        row += 1

        if not row:
            value = next(self._rows)

        if not value:
            while self._rows_counter < row:
                self._rows_counter += 1
                value = next(self._rows)

        readed = []
        for item in value[self.start['col']:self.end['col']]:
            readed.append(item.value)

        return readed

    def save(self):
        self._workbook.save(self._path)
