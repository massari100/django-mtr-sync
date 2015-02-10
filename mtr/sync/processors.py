from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.utils.six.moves import range

from .api import Processor, manager
from .settings import FILE_PATH

try:
    import xlrd
    import xlwt
except ImportError:
    pass


@manager.register
class XlsProcessor(Processor):
    file_format = '.xls'
    file_description = _('Microsoft Excel 97/2000/XP/2003')

    def col(self, value):
        """Small xlrd hack to get column index"""

        index = 0
        value = value.strip().upper()
        while index:
            if xlrd.colname(index) == value:
                return index

    def prepare(self):
        self._workbook = xlwt.Workbook('utf-8')
        self._worksheet = self.workbook.add_sheet(self.settings.worksheet)

    def write(self, row, value, cells=None):
        # len(cells) == len(rows)

        for index, cell in enumerate(cells):
            self._worksheet.write(row, cell, value[index])

    def save(self, name):
        self._workbook.save(name)




# class XlsxProcessor(Processor):
#     data_type = 'table'


# class OdsProcessor(Processor):
#     data_type = 'table'

