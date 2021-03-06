import os

import ezodf

from ..processor import Processor
from ..manager import manager
from ...translation import gettext_lazy as _


@manager.register('processor')
class OdsProcessor(Processor):
    file_format = '.ods'
    file_description = _('ODF Spreadsheet')

    def create(self, path):
        self._path = path
        self._max_cells = max(self.cells)
        self._workbook = ezodf.newdoc(doctype='ods', filename=path)
        self._worksheet = ezodf.Table(
            self.settings.worksheet,
            size=(self.end['row'], self._max_cells + 1))
        self._workbook.sheets.append(self._worksheet)

    def open(self, path):
        ezodf.config.set_table_expand_strategy('all')

        self._path = path
        self._workbook = ezodf.opendoc(self._path)

        ezodf.config.reset_table_expand_strategy()

        if not self.settings.worksheet:
            self.settings.worksheet = self._workbook.sheets[0].name

        self._worksheet = self._workbook.sheets[self.settings.worksheet]

        return self._worksheet.nrows(), self._worksheet.ncols()

    def write(self, row, value):
        for index, cell in enumerate(self.cells):
            self._worksheet[row, cell].set_value(
                '' if value[index] is None else value[index])

    def read(self, row, cells=None):
        readed = []
        cells = cells or self.cells

        for index, cell in enumerate(cells):
            try:
                readed.append(self._worksheet[row, cell].value)
            except IndexError:
                readed.append('')

        return readed

    def save(self):
        self._workbook.save()

        try:
            os.remove('{}.bak'.format(self._path))
        except OSError:
            pass
