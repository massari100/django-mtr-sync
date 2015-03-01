from __future__ import unicode_literals

from django.test import TestCase

from mtr.sync.tests import ProcessorTestMixin
from mtr.sync.api.processors import xls, xlsx, csv, ods

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

    def _get_row_values(self, row, rows):
        for index, value in enumerate(rows):
            if index == row and row:
                return value

    def check_values(self, worksheet, instance, row, index_prepend=0):
        row_values = self._get_row_values(row, worksheet.iter_rows())

        for index, field in enumerate(self.fields):
            value = getattr(instance, field.attribute)
            sheet_value = row_values[index + index_prepend].value

            self.assertEqual(value, sheet_value)


class CsvProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    PROCESSOR = csv.CsvProcessor

    def open_report(self, report):
        self._f = open(report.buffer_file.path)

        return csv.csv.reader(self._f)

    def _get_row_values(self, row, reader):
        for index, value in enumerate(reader):
            if index == row and row:
                return value

    def check_values(self, reader, instance, row, index_prepend=0):
        row_values = self._get_row_values(row, reader)

        for index, field in enumerate(self.fields):
            value = getattr(instance, field.attribute)
            sheet_value = self.processor._convert(
                row_values[index + index_prepend])

            self.assertEqual(value, sheet_value)

        self._f.close()


class OdsProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    PROCESSOR = ods.OdsProcessor

    def open_report(self, report):
        workbook = ods.ezodf.opendoc(report.buffer_file.path)
        worksheet = workbook.sheets[self.settings.worksheet]

        return worksheet

    def check_values(self, worksheet, instance, row, index_prepend=0):
        row_values = worksheet.row(row)

        for index, field in enumerate(self.fields):
            value = getattr(instance, field.attribute)
            sheet_value = row_values[index + index_prepend].value

            self.assertEqual(value, sheet_value)
