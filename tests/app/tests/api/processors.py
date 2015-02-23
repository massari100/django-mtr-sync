from __future__ import unicode_literals

from django.test import TestCase

from mtr.sync.tests import ProcessorTestMixin
from mtr.sync.api.processors import xls, xlsx, csv

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


class XlsxProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    PROCESSOR = xlsx.XlsxProcessor

    def open_report(self, report):
        workbook = xlsx.openpyxl.load_workbook(
            report.buffer_file.path, use_iterators=True)
        worksheet = workbook.get_sheet_by_name(self.settings.worksheet)
        return worksheet

    def get_row_values(self, row, current_row):
        for index, value in enumerate(current_row):
            if index == row and row:
                return value

    def check_values(self, worksheet, instance, row, index_prepend=0):
        row_values = self.get_row_values(row, worksheet.iter_rows())

        for index, field in enumerate(self.fields):
            value = getattr(instance, field.attribute)
            sheet_value = row_values[index + index_prepend].value

            self.assertEqual(value, sheet_value)


class CsvProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    PROCESSOR = csv.CsvProcessor

    # def open_report(self, report):
    #     workbook = xlsx.openpyxl.load_workbook(
    #         report.buffer_file.path, use_iterators=True)
    #     worksheet = workbook.get_sheet_by_name(self.settings.worksheet)
    #     return worksheet

    # def get_row_values(self, row, current_row):
    #     for index, value in enumerate(current_row):
    #         if index == row and row:
    #             return value

    # def check_values(self, worksheet, instance, row, index_prepend=0):
    #     row_values = self.get_row_values(row, worksheet.iter_rows())

    #     for index, field in enumerate(self.fields):
    #         value = getattr(instance, field.attribute)
    #         sheet_value = row_values[index + index_prepend].value

    #         self.assertEqual(value, sheet_value)
