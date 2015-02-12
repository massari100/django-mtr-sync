import os
import datetime

from django.test import TestCase
from django.utils.six.moves import range

from ..api.manager import Manager
from ..api.processors import Processor, XlsProcessor
from ..models import Settings


class TestProcessor(Processor):
    pass


class ManagerTest(TestCase):
    def setUp(self):
        self.manager = Manager.create()
        self.manager.register(XlsProcessor)

    def test_registering_and_unregistering_processor(self):
        self.manager.register(TestProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), True)

        self.manager.unregister(TestProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), False)

    def test_export_data_and_report_generation(self):
        settings = Settings(
            processor=XlsProcessor.__name__, worksheet='test')
        data = {'rows': 10, 'cols': 2, 'items': iter(range(0, 2*10))}
        report = self.manager.export_data(settings, data)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertEqual(os.path.exists(report.buffer_file.path), True)
        self.assertEqual(os.path.getsize(report.buffer_file.path) > 0, True)
        self.assertEqual(os.remove(report.buffer_file.path), None)
