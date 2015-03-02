from __future__ import unicode_literals

import os
import datetime

from django.test import TestCase

from mtr.sync.api import Manager, Processor
from mtr.sync.models import Settings, Filter, FilterParams


class ProcessorTestMixin(object):
    MODEL = None
    PROCESSOR = None
    MODEL_COUNT = 50

    def setUp(self):
        self.model = self.MODEL

        self.manager = Manager()
        self.manager.register('processor', self.PROCESSOR)

        self.instance = self.model.objects.create(name='test instance',
            surname='test surname', gender='M', security_level=10)
        self.instance.populate(self.MODEL_COUNT)
        self.queryset = self.model.objects.all()

        self.settings = Settings.objects.create(
            action=Settings.EXPORT,
            processor=self.PROCESSOR.__name__, worksheet='test',
            main_model='{}.{}'.format(
                self.model.__module__, self.model.__name__),
            include_header=False)
        self.processor = self.manager.make_processor(self.settings)

        self.fields = self.settings.create_default_fields()

    def check_file_existence_and_delete(self, report):
        """Delete report file"""

        self.assertIsNone(os.remove(report.buffer_file.path))

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
        start_row = self.settings.start_row - 1
        end_row = self.settings.end_row - 1
        start_col = self.processor.column(self.settings.start_col) - 1

        fields_limit = self.settings.end_col - \
            self.processor.column(self.settings.start_col) + 1
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

    def test_export_dimension_settings(self):
        self.settings.start_row = 25
        self.settings.start_col = 'J'
        self.settings.end_col = 12
        self.settings.end_row = 250

        report = self.check_report_success(delete=False)

        self.check_sheet_values_and_delete_report(report)

    def test_import_data(self):
        # TODO: refactor code to works with values smaller then 3
        # e.g. start_row = 1

        self.settings.start_row = 3
        self.settings.start_col = 10
        self.settings.end_col = 13
        self.settings.end_row = 250

        report = self.check_report_success(delete=False)

        before = self.settings.end_row - self.settings.start_row + 1
        if before > self.queryset.count():
            before = self.queryset.count()

        self.queryset.delete()

        self.settings.action = self.settings.IMPORT
        self.settings.buffer_file = report.buffer_file

        self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report)

        self.assertEqual(before, self.queryset.count())

    def test_value_filters(self):
        before_data = list(self.manager.prepare_export_data(
            self.processor, self.queryset)['items'])

        @self.manager.register('filter', label='multiply by 10')
        def test_filter(value, field, action):
            if value.isnumber():
                value *= 10
            return value

        filter_related = Filter.objects.get(name='test_filter')
        field_related = self.fields.get(attribute='id')
        FilterParams.objects.create(
            filter_related=filter_related, field_related=field_related)

        after_data = self.manager.prepare_export_data(
            self.processor, self.queryset)['items']

        for before_item, after_item in zip(before_data, after_data):
            if isinstance(before_item, int) or before_item.isnumber():
                self.assertEqual(before_item, after_item / 10)


class ProcessorTest(TestCase):

    def setUp(self):
        self.manager = Manager()
        self.processor = Processor(self.manager, None)

    def test_column_index_value_transform(self):
        self.assertEqual(
            self.processor.column_name(0), 'A')
        self.assertEqual(
            self.processor.column_name(25), 'Z')

        self.assertEqual(
            self.processor.column_index('A'), 0)
        self.assertEqual(
            self.processor.column_index('Z'), 25)
