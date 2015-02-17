from __future__ import unicode_literals

import os
import datetime

from django.test import TestCase
from django.utils.six.moves import range

from mtr.sync.api import Manager
from mtr.sync.api.processors.xlsx import XlsxProcessor
from mtr.sync.models import Settings

from ....models import Person


class ManagerTest(TestCase):
    def setUp(self):
        self.model = Person

        self.manager = Manager()
        self.manager.register(XlsxProcessor)

        self.instance = self.model.objects.create(name='test instance',
            surname='test surname', gender='M', security_level=10)
        self.instance.populate(50000)
        self.queryset = self.model.objects.all()

        print 'QUERYSET CREATED!'

        self.settings = Settings.objects.create(
            action=Settings.EXPORT,
            processor=XlsxProcessor.__name__, worksheet='test',
            main_model='{}.{}'.format(
                self.model.__module__, self.model.__name__))

        self.settings.create_default_fields()

    def test_export_data_and_report_generation(self):
        report = self.manager.export_data(self.settings)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertTrue(os.path.exists(report.buffer_file.path))
        self.assertTrue(os.path.getsize(report.buffer_file.path) > 0)
        # self.assertIsNone(os.remove(report.buffer_file.path))
