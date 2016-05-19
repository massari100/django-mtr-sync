from __future__ import unicode_literals

from django.test import TestCase
from django.utils.encoding import smart_text

from mtr.sync.tests import ProcessorTestMixin
from mtr.sync.lib.helpers import process_attribute
from mtr.sync.lib.processor import Processor
from mtr.sync.lib.processors import xls, xlsx, csv, ods

from ...models import Person, Office, Tag


class XlsProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = xls.XlsProcessor

    def open_report(self, report):
        workbook = xls.xlrd.open_workbook(report.buffer_file.path)
        worksheet = workbook.sheet_by_name(self.settings.worksheet)

        return worksheet

    def check_values(self, worksheet, instance, row):
        for index, field in enumerate(self.fields):
            value = process_attribute(instance, field.attribute)
            try:
                sheet_value = worksheet.cell_value(row, index)
            except IndexError:
                sheet_value = ''

            if isinstance(value, list):
                value = ','.join(smart_text(v) for v in value)
            elif value:
                value = smart_text(value)

            self.assertEqual(
                '' if value is None else value,
                '' if sheet_value is None else sheet_value)


class XlsxProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = xlsx.XlsxProcessor

    def open_report(self, report):
        workbook = xlsx.openpyxl.load_workbook(
            report.buffer_file.path, use_iterators=True)
        worksheet = workbook.get_sheet_by_name(self.settings.worksheet)

        return worksheet

    def _get_row_values(self, row, rows):
        for index, value in enumerate(rows):
            if index == row:
                return value

    def check_values(self, worksheet, instance, row):
        row_values = self._get_row_values(row, worksheet.iter_rows())

        for index, field in enumerate(self.fields):
            value = process_attribute(instance, field.attribute)
            sheet_value = row_values[index].value
            sheet_value = '' if sheet_value is None else sheet_value

            if isinstance(value, list):
                value = ','.join(smart_text(v) for v in value)
            elif value:
                value = smart_text(value)

            self.assertEqual(
                '' if value is None else value,
                '' if sheet_value is None else sheet_value)


class CsvProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = csv.CsvProcessor

    def open_report(self, report):
        self._f = open(report.buffer_file.path)

        return csv.csv.reader(self._f)

    def _get_row_values(self, row, worksheet):
        for index, value in enumerate(worksheet):
            if index == row:
                return value

    def check_values(self, worksheet, instance, row):
        row_values = self._get_row_values(row, worksheet)

        for index, field in enumerate(self.fields):
            value = process_attribute(instance, field.attribute)
            sheet_value = row_values[index]

            if isinstance(value, list):
                value = ','.join(smart_text(v) for v in value)
            elif value:
                value = smart_text(value)

            self.assertEqual(
                '' if value is None else value,
                '' if sheet_value is None else sheet_value)

        self._f.close()


class OdsProcessorTest(ProcessorTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = ods.OdsProcessor

    def open_report(self, report):
        workbook = ods.ezodf.opendoc(report.buffer_file.path)
        worksheet = workbook.sheets[self.settings.worksheet]

        return worksheet

    def check_values(self, worksheet, instance, row):
        row_values = worksheet.row(row)

        for index, field in enumerate(self.fields):
            value = process_attribute(instance, field.attribute)
            sheet_value = row_values[index].value

            if isinstance(value, list):
                value = ','.join(smart_text(v) for v in value)
            elif value:
                value = smart_text(value)

            self.assertEqual(
                '' if value is None else value,
                '' if sheet_value is None else sheet_value)


class ProcessorTest(TestCase):

    def setUp(self):
        class SomeProcessor(Processor):
            pass

        self.processor = SomeProcessor(None, None)

    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.processor.write(0)
        with self.assertRaises(NotImplementedError):
            self.processor.read(0)
        with self.assertRaises(NotImplementedError):
            self.processor.create('')
        with self.assertRaises(NotImplementedError):
            self.processor.open('')
        with self.assertRaises(NotImplementedError):
            self.processor.save()
