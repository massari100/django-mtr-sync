from django.utils.translation import gettext_lazy as _

import csv

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class CsvProcessor(Processor):
    file_format = '.csv'
    file_description = _('mtr.sync:CSV (;)')

    def column_index(self, value):
        # TODO: csv warning index only in settings

        return value

    def create(self, path):
        # TODO: csv additional settings

        self._prepend = None
        self._f = open(path)
        self._writer = csv.writer(self._f)

        # prepend rows and cols
        if self.start['row'] > 0:
            for i in range(0, self.start['row']):
                self._writer.writerow([])

        if self.start['col'] > 0:
            self._prepend = [None, ]
            self._prepend *= self.start['col']

    def open(self, path):
        f = open(path)

        self._reader = csv.reader(f)

        maxrows = 0
        maxcols = 0

        return maxrows, maxcols

    def write(self, row, value):
        if self._prepend:
            value = self._prepend + value

        self._writer.writerow(value[:self.end['col']])

    def read(self, row):
        data = []
        for cell in self.cells:
            data.append(self._worksheet.cell_value(row, cell))
        return data

    def save(self):
        self._f.close()
