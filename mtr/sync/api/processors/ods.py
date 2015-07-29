import os

import ezodf

from ..processor import Processor
from ..manager import manager
from ...helpers import gettext_lazy as _


@manager.register('processor')
class OdsProcessor(Processor):
    file_format = '.ods'
    file_description = _('ODF Spreadsheet')

    def create(self, path):
        self.path = path
        # self.max_cells = max(self.cells)

        self.workbook = ezodf.newdoc(doctype='ods', filename=path)

        if self.settings:
            self.worksheet = ezodf.Table(self.settings.worksheet)
            # size=(self.end['row'], self._max_cells + 1))
            self.workbook.sheets.append(self._worksheet)

        return self.workbook

    def open(self, path):
        ezodf.config.set_table_expand_strategy('all')

        self.path = path
        self.workbook = ezodf.opendoc(self.path)

        ezodf.config.reset_table_expand_strategy()

        if self.settings:
            if not self.settings.worksheet:
                self.settings.worksheet = self.workbook.sheets[0].name

            self.worksheet = self.workbook.sheets[self.settings.worksheet]

            self.nrows = self.worksheet.nrows()
            self.ncols = self.worksheet.ncols()

    def write(self, row, value):
        for index, cell in enumerate(self.cells):
            self.worksheet[row, cell].set_value(
                '' if value[index] is None else value[index])

    def read(self, row, cells=None):
        readed = []
        cells = cells or self.cells

        for index, cell in enumerate(cells):
            try:
                readed.append(self.worksheet[row, cell].value)
            except IndexError:
                readed.append('')

        return readed

    def save(self, path=None):
        path = path or self.path

        self.workbook.save(path)

        try:
            os.remove('{}.bak'.format(path))
        except OSError:
            pass
