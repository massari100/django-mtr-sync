# coding: utf-8

from __future__ import unicode_literals

import os
import datetime

from django.utils import six

from mtr.sync.api import Manager
from mtr.sync.api.helpers import column_value
from mtr.sync.models import Settings


class ApiTestMixin(object):
    MODEL = None
    RELATED_MODEL = None
    RELATED_MANY = None
    PROCESSOR = None
    MODEL_COUNT = 10
    CREATE_PROCESSOR_AT_SETUP = True

    def setUp(self):
        self.model = self.MODEL
        self.relatedmodel = self.RELATED_MODEL

        self.manager = Manager()

        if self.CREATE_PROCESSOR_AT_SETUP:
            self.manager.register('processor', self.PROCESSOR)

        self.instance = self.model.objects.create(
            name=six.text_type('test instance éprouver'),
            surname='test surname',
            gender='M', security_level=10)
        self.r_instance = self.relatedmodel.objects.create(
            office='test', address='addr')
        self.tags = [
            self.RELATED_MANY(name='test'), self.RELATED_MANY(name='test1')]

        for tag in self.tags:
            tag.save()
            self.instance.tags.add(tag)

        self.instance.office = self.r_instance
        self.instance.save()

        self.instance.populate(self.MODEL_COUNT)
        self.queryset = self.model.objects.all()

        self.settings = Settings.objects.create(
            action=Settings.EXPORT,
            processor=self.PROCESSOR.__name__, worksheet='test',
            main_model='{}.{}'.format(
                self.model.__module__, self.model.__name__),
            include_header=False)

        if self.CREATE_PROCESSOR_AT_SETUP:
            self.processor = self.manager.make_processor(self.settings)

            self.fields = self.settings.create_default_fields()


class ProcessorTestMixin(ApiTestMixin):

    def check_file_existence_and_delete(self, report):
        """Delete report file"""
        pass
        # self.assertIsNone(os.remove(report.buffer_file.path))

    def check_report_success(self, delete=True):
        """Create report from settings and assert it's successful"""

        report = self.manager.export_data(self.settings)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertTrue(os.path.exists(report.buffer_file.path))
        self.assertTrue(os.path.getsize(report.buffer_file.path) > 0)

        if delete:
            self.check_file_existence_and_delete(report)

        return report

    def check_sheet_values_and_delete_report(self, report):
        if self.settings.start_row:
            start_row = self.settings.start_row - 1
        else:
            start_row = 0

        if self.settings.end_row:
            end_row = self.settings.end_row - 1
        else:
            end_row = self.queryset.count() - 1

        if self.settings.start_col:
            start_col = column_value(self.settings.start_col) - 1
        else:
            start_col = 0

        if self.settings.start_col and self.settings.end_col:
            fields_limit = self.settings.end_col - \
                column_value(self.settings.start_col) + 1
        else:
            fields_limit = len(self.fields)

        self.fields = self.fields[:fields_limit]

        if self.queryset.count() < end_row:
            end_row = self.queryset.count() + start_row - 1

        worksheet = self.open_report(report)
        self.check_values(
            worksheet, self.queryset.first(), start_row, start_col)

        worksheet = self.open_report(report)
        self.check_values(
            worksheet, self.queryset.get(pk=end_row - start_row + 1),
            end_row, start_col)

        self.check_file_existence_and_delete(report)

    def open_report(self, report):
        """Open data file and return worksheet or other data source"""

        raise NotImplementedError

    def check_values(self, worksheet, instance, row, index_prepend=0):
        """Check instance values within data"""

        raise NotImplementedError

    def test_create_export_file_and_report_generation(self):
        self.check_report_success()

    def test_export_all_dimension_settings(self):
        self.settings.start_row = 25
        self.settings.start_col = 'J'
        self.settings.end_col = 20
        self.settings.end_row = 250

        report = self.check_report_success(delete=False)

        self.check_sheet_values_and_delete_report(report)

    def test_export_no_dimension_settings(self):
        report = self.check_report_success(delete=False)

        self.check_sheet_values_and_delete_report(report)

    def test_import_data(self):
        self.settings.start_row = 1
        self.settings.start_col = 10
        self.settings.end_col = 20
        self.settings.end_row = 250

        report = self.check_report_success(delete=False)

        before = self.settings.end_row - self.settings.start_row + 1
        if before > self.queryset.count():
            before = self.queryset.count()

        self.queryset.delete()
        for tag in self.tags:
            tag.delete()

        self.settings.action = self.settings.IMPORT
        self.settings.buffer_file = report.buffer_file

        self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report)

        self.assertEqual(before, self.queryset.count())

    def test_reading_empty_values(self):
        report = self.check_report_success(delete=False)

        max_rows, max_cols = self.processor.open(report.buffer_file.path)
        self.processor.set_dimensions(0, 0,
            max_rows, max_cols, import_data=True)

        self.assertEqual(
            self.processor.end['col'], len(self.processor.read(10000)))

        self.assertEqual(
            ['', '', ''], self.processor.read(10000, [0, 23543, 434]))
