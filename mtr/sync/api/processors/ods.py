from django.utils.translation import gettext_lazy as _

import ezodf

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class OdsProcessor(Processor):
    file_format = '.ods'
    file_description = _('mtr.sync:ODF Spreadsheet')

    def create(self, path):
        self._path = path
        self._prepend = None
        self._workbook = ezodf.newdoc(doctype='ods', filename=path)
        self._worksheet = ezodf.Table(self.settings.worksheet)
        self._workbook.sheets.append(self._worksheet)

        # prepend rows and cols
        # TODO: strange bug exposes only when start_row = 25 and test passed
        if self.start['row'] > 11:
            self._worksheet.append_rows(self.start['row'] - 10)

        if self.start['col'] > 0:
            self._worksheet.append_columns(self.start['col'])

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
        self._worksheet.append_rows(1)

        for index, cell in enumerate(self.cells):
            self._worksheet[row, cell].set_value(value[index])

    def read(self, row):
        readed = []
        for index, cell in enumerate(self.cells):
            readed.append(self._worksheet[row, cell].value)

        return readed

    def save(self):
        self._workbook.save()
