from __future__ import unicode_literals

import os
import datetime

from mtr.sync.api import Manager
from mtr.sync.models import Settings


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

    def open_report(self, report):
        """Open data file and return worksheet or other data source"""

        raise NotImplementedError

    def test_create_export_file_and_report_generation(self):
        self.check_report_success()

    def test_export_dimension_settings(self):
        self.settings.start_row = 25
        self.settings.start_col = 10
        self.settings.end_col = 12
        self.settings.end_row = 250

        report = self.check_report_success(delete=False)
        worksheet = self.open_report(report)

        start_row = self.settings.start_row - 1
        end_row = self.settings.end_row - 1
        start_col = self.settings.start_col - 1

        fields_limit = self.settings.end_col - self.settings.start_col + 1
        self.fields = self.fields[:fields_limit]

        if self.queryset.count() < end_row:
            end_row = self.queryset.count() + start_row - 1

        self.check_values(
            worksheet, self.queryset.first(), start_row, start_col)
        self.check_values(
            worksheet, self.queryset.get(pk=end_row - start_row + 1),
            end_row, start_col)

        self.check_file_existence_and_delete(report)

    # TODO: add import test with dimensions
