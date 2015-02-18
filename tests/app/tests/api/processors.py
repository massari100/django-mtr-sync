from __future__ import unicode_literals

from django.test import TestCase

from mtr.sync.tests import ProcessorTestMixin
from mtr.sync.api.processors import xls, xlsx

from ...models import Person


class XlsProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    PROCESSOR = xls.XlsProcessor

    def open_report(self, report):
        workbook = xls.xlrd.open_workbook(report.buffer_file.path)
        worksheet = workbook.sheet_by_name(self.settings.worksheet)

        return worksheet

    def check_values(self, worksheet, instance, row, index_prepend=0):
        for index, field in enumerate(self.fields):
            value = getattr(instance, field.attribute)

            sheet_value = worksheet.cell_value(row, index+index_prepend)

            self.assertEqual(value, sheet_value)


# class XlsxProcessorTest(ProcessorTestMixin, TestCase):
#     MODEL = Person
#     PROCESSOR = xlsx.XlsxProcessor

#     def open_report(self, report):
#         workbook = xlsx.openpyxl.load_workbook(
#             report.buffer_file.path, use_iterators=True)
#         worksheet = workbook.get_sheet_by_name(self.settings.worksheet)
#         return worksheet

#     def check_values(self, worksheet, instance, row, index_prepend=0):
        # self._current_row = getattr(
        #     self, '_current_row', worksheet.iter_rows())

        # row_values = []
        # for index, field in enumerate(self.fields):
        #     row_values.append(getattr(instance, field.attribute))


        # for row in worksheet.iter_rows(): # it brings a new method: iter_rows()

        #     for cell in row:

        #         print cell.value

        # row_value = next(self._current_row)
        # while row > self._current_row.index:
        #     row_value = next(self._current_row)

        # print row_value

        # sheet_value = worksheet.cell_value(row, index+index_prepend)

        # self.assertEqual(value, sheet_value)
