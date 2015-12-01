from __future__ import absolute_import

from django.utils import six

if six.PY2:
    import unicodecsv as csv
else:
    import csv

from ..processor import Processor
from ..manager import manager
from ...translation import gettext_lazy as _


@manager.register('processor')
class CsvProcessor(Processor):
    file_format = '.csv'
    file_description = _('CSV')

    def create(self, path):
        # TODO: csv additional settings

        self._prepend = None
        self._f = open(path, 'w')
        self._writer = csv.writer(self._f, dialect='excel')

        # prepend rows
        if self.start['row'] > 1:
            for i in range(0, self.start['row']):
                self._writer.writerow([])

    def open(self, path):
        self._f = open(path, 'r')
        self._reader = csv.reader(self._f, dialect='excel')
        self._rows_counter = 0

        maxrows = 0
        maxcols = 0

        for row in self._reader:
            maxrows += 1
            if len(row) > maxcols:
                maxcols = len(row)
        self._max_cells = maxcols

        self._f.seek(0)

        return maxrows, maxcols

    def write(self, row, value):
        if self._prepend:
            value = self._prepend + value

        self._writer.writerow(value)

    def _get_row(self, row):
        value = None
        row += 1

        try:
            while self._rows_counter < row:
                self._rows_counter += 1
                value = next(self._reader)
        except StopIteration:
            return [''] * (self._max_cells + 1)

        return value

    def read(self, row, cells=None):
        readed = []
        value = self._get_row(row)
        cells = cells or self.cells

        for index in cells:
            # TODO: value convert

            try:
                item = value[index]
                if item.isdigit():
                    item = int(item)
                readed.append(item)
            except IndexError:
                readed.append('')

        return readed

    def save(self):
        self._f.close()
