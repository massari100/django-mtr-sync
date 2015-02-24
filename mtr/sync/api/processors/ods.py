from django.utils.translation import gettext_lazy as _

import odf


class OdsProcessor(Processor):
    file_format = '.ods'
    file_description = _('mtr.sync:ODF Spreadsheet')

    def create(self):
        self._workbook = odf.opendocument.OpenDocumentSpreadsheet()
        self._table = odf.table.Table(self.worksheet.name)
        self._worksheet = self._workbook.spreadsheet.addElement(self._table)

    def open(self):
        self._workbook = xlrd.open_workbook(self.settings.buffer_file)
        self._worksheet = self._workbook(self.settings.worksheet)

    def write(self, row, value):
        table_row = odf.table.TableRow()
        self._table.addElement(table_row)
        for index, cell in enumerate(self.cells):
            table_cell = odf.table.TableCell()
            table_row =
            self._worksheet.write(row, cell, value[index])

    def read(self, row):
        for index, cell in enumerate(self.cells):
            yield self._worksheet.cell_value(row, cell)

    def save(self, name):
        self._workbook.save(name)
