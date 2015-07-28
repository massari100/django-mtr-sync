import xlrd
import xlwt

from ..processor import Processor
from ..manager import manager
from ...helpers import gettext_lazy as _


@manager.register('processor')
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('Microsoft Excel 97/2000/XP/2003')

    def create(self, path):
        self.path = path
        self.workbook = xlwt.Workbook('utf-8')

        if self.settings:
            self.worksheet = self.workbook.add_sheet(self.settings.worksheet)

        return self.workbook

    def open(self, path):
        self.workbook = xlrd.open_workbook(path)

        if self.settings:
            if not self.settings.worksheet:
                self.settings.worksheet = self.workbook.sheet_names()[0]

            self.worksheet = \
                self.workbook.sheet_by_name(self.settings.worksheet)

            self.nrows, self.ncols = \
                self.worksheet.nrows, self.worksheet.ncols

        return self.worksheet

    def write(self, row, value, cells=None):
        cells = self.cells or cells or len(row)
        for index, cell in enumerate(self.cells):
            self.worksheet.write(
                row, cell,
                '' if value[index] is None else value[index])

    def read(self, row, cells=None):
        data = []
        cells = cells or self.cells or len(row)

        for cell in cells:
            try:
                data.append(self.worksheet.cell_value(row, cell))
            except IndexError:
                data.append('')

        return data

    def save(self, path=None):
        path = path or self.path

        self.workbook.save(path)
