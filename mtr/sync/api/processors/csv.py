from django.utils.translation import gettext_lazy as _

import csv

from ..processor import Processor
from ..manager import manager


@manager.register('processor')
class CsvProcessor(Processor):
    file_format = '.csv'
    file_description = _('mtr.sync:CSV (;)')

    def create(self, path):
        # TODO: csv additional settings

        self._prepend = None
        self._f = open(path, 'w')
        self._writer = csv.writer(self._f)

        # prepend rows and cols
        if self.start['row'] > 0:
            for i in range(0, self.start['row']):
                self._writer.writerow([])

        if self.start['col'] > 0:
            self._prepend = [None, ]
            self._prepend *= self.start['col']

    def open(self, path):
        self._f = open(path, 'r')
        self._reader = csv.reader(self._f)
        self._rows_counter = 0

        maxrows = 0
        maxcols = 0

        for row in self._reader:
            maxrows += 1
            if len(row) > maxcols:
                maxcols = len(row)

        self._f.seek(0)

        return maxrows, maxcols

    def write(self, row, value):
        if self._prepend:
            value = self._prepend + value

        self._writer.writerow(value[:self.end['col']])

    def read(self, row):
        value = None
        row += 1

        if not row:
            value = next(self._reader)

        if not value:
            while self._rows_counter < row:
                self._rows_counter += 1
                value = next(self._reader)

        readed = []
        for item in value[self.start['col']:self.end['col']]:
            readed.append(item)
        return readed

    def save(self):
        self._f.close()
