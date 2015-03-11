import xlrd
import xlwt

from django.utils.translation import gettext_lazy as _

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('mtr.sync:Microsoft Excel 97/2000/XP/2003')

    def create(self, path):
        self._path = path
        self._workbook = xlwt.Workbook('utf-8')
        self._worksheet = self._workbook.add_sheet(self.settings.worksheet)

    def open(self, path):
        self._workbook = xlrd.open_workbook(path)

        if not self.settings.worksheet:
            self.settings.worksheet = self._workbook.sheet_names()[0]

        self._worksheet = self._workbook.sheet_by_name(self.settings.worksheet)

        return self._worksheet.nrows, self._worksheet.ncols

    def write(self, row, value):
        for index, cell in enumerate(self.cells):
            self._worksheet.write(
                row, cell,
                '' if value[index] is None else value[index])

    def read(self, row):
        data = []
        for cell in self.cells:
            try:
                data.append(self._worksheet.cell_value(row, cell))
            except IndexError:
                data.append('')

        return data

    def save(self):
        self._workbook.save(self._path)
