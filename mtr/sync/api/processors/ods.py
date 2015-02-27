from django.utils.translation import gettext_lazy as _

import odf
import odf.opendocument
import odf.table
import odf.text

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class OdsProcessor(Processor):
    file_format = '.ods'
    file_description = _('mtr.sync:ODF Spreadsheet')

    def create(self, path):
        self._path = path
        self._workbook = odf.opendocument.OpenDocumentSpreadsheet()
        self._table = odf.table.Table(name=self.settings.worksheet)
        self._worksheet = self._workbook.spreadsheet.addElement(self._table)

    def open(self, path):
        self._path = path
        self._workbook = odf.opendocument.load(self._path)

        # TODO: get element by type Table, iter childs and convert values

    def write(self, row, value):
        table_row = odf.table.TableRow()
        self._table.addElement(table_row)

        for index, cell in enumerate(self.cells):
            table_cell = odf.table.TableCell()
            table_row.addElement(table_cell)
            table_cell.addElement(odf.text.P(text=value[index]))

    def read(self, row):
        for index, cell in enumerate(self.cells):
            yield self._worksheet.cell_value(row, cell)

    def save(self):
        self._workbook.save(self._path)
